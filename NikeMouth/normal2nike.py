import numpy as np
import cv2
import face_recognition


# 繪製delaunay triangles
def draw_delaunay(img, TriangleList, delaunary_color):
    
    size = img.shape
    r = (0, 0, size[1], size[0])
    
    for t in TriangleList:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
    
        # if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
        cv2.line(img, pt1, pt2, delaunary_color, 1)
        cv2.line(img, pt2, pt3, delaunary_color, 1)
        cv2.line(img, pt3, pt1, delaunary_color, 1)

def get_Ms(t1,t2):
    Ms = []
    for i in range(len(t1)):
        pts1 = np.array([[t1[i][0],t1[i][1]],[t1[i][2],t1[i][3]],[t1[i][4],t1[i][5]]]).astype(np.float32)
        pts2 = np.array([[t2[i][0],t2[i][1]],[t2[i][2],t2[i][3]],[t2[i][4],t2[i][5]]]).astype(np.float32)
        # print(pts1)
        Ms.append(cv2.getAffineTransform(pts1,pts2))
    return Ms

def delaunay(h,w,points):
    subdiv = cv2.Subdiv2D((0,0,w,h))
    for i in range(len(points)):
        subdiv.insert(tuple(points[i]))
    TriangleList = subdiv.getTriangleList()
    return TriangleList

def get_borderpoints(img):
    h,w = img.shape[:2]
    h,w = h-1,w-1
    points = [[0,0],[w//2,0],[w,0],[w,h//2],[w,h],[w//2,h],[0,h],[0,h//2]]
    return np.array(points)

def get_masks(img,t):
    masks = np.zeros((len(t),img.shape[0],img.shape[1]), dtype=np.uint8)
    for i in range(len(t)):

        points = np.array([[t[i][0],t[i][1]],[t[i][2],t[i][3]],[t[i][4],t[i][5]]]).astype(np.int64)
        #print(points)
        masks[i] = cv2.fillConvexPoly(masks[i],points,(255))
        cv2.line(masks[i], tuple(points[0]), tuple(points[1]), (255), 3)
        cv2.line(masks[i], tuple(points[0]), tuple(points[2]), (255), 3)
        cv2.line(masks[i], tuple(points[1]), tuple(points[2]), (255), 3)

        #masks[i] = cv2.drawContours(masks[i], points, contourIdx=0, color=255, thickness=2)
    return masks

def changeTriangleList(t,point,move):
    t = t.astype(np.int64)
    for i in range(len(t)):
        if t[i][0]==point[0] and t[i][1]==point[1]:
            t[i][0],t[i][1] = t[i][0]+move[0],t[i][1]+move[1]
        elif t[i][2]==point[0] and t[i][3]==point[1]:
            t[i][2],t[i][3] = t[i][2]+move[0],t[i][3]+move[1]
        elif t[i][4]==point[0] and t[i][5]==point[1]:
            t[i][4],t[i][5] = t[i][4]+move[0],t[i][5]+move[1]
    return t

def replace_delaunay(img,Ms,masks):
    img_new  = np.zeros_like(img)
    h,w = img.shape[:2]
    for i in range(len(Ms)):
        # _img = img.copy()
        mask = cv2.merge([masks[i], masks[i], masks[i]])
        mask_inv = cv2.bitwise_not(mask)
        tmp = cv2.warpAffine(img,Ms[i],(w,h),borderMode = cv2.BORDER_REFLECT_101,flags=cv2.INTER_CUBIC)
        tmp = cv2.bitwise_and(mask,tmp)
        img_new = cv2.bitwise_and(mask_inv,img_new)
        img_new = cv2.add(tmp,img_new)
    return img_new

def get_nikemouth_landmark(src_landmark,alpha=1,aspect_ratio=1.0,mode = 'only_mouth'):


    nike = cv2.imread('./imgs/nike.png')
    landmark = face_recognition.face_landmarks(nike)[0]
    if mode == 'only_mouth':
        src_landmark = src_landmark[56:]
        nikemouth = np.array(landmark['top_lip']+landmark['bottom_lip'])
    else:
        src_landmark = src_landmark[25:]
        nikemouth = np.array(landmark['left_eyebrow']+landmark['right_eyebrow']+landmark['nose_bridge']+\
            landmark['nose_tip']+landmark['left_eye']+landmark['right_eye']+landmark['top_lip']+\
            landmark['bottom_lip'])

    # 中心置0
    nikemouth = nikemouth-[np.mean(nikemouth[:,0]),np.mean(nikemouth[:,1])]
    nikemouth[:,0] = nikemouth[:,0]*aspect_ratio
    # 获取嘴巴大小
    nikemouth_h = np.max(nikemouth[:,1])-np.min(nikemouth[:,1])
    nikemouth_w = np.max(nikemouth[:,0])-np.min(nikemouth[:,0])
    src_h = np.max(src_landmark[:,1])-np.min(src_landmark[:,1])
    src_w = np.max(src_landmark[:,0])-np.min(src_landmark[:,0])

    # 调整大小及位置
    beta = nikemouth_w/src_w
    nikemouth = alpha*nikemouth/beta+[np.mean(src_landmark[:,0]),np.mean(src_landmark[:,1])]
    return np.around(nikemouth,0)



def convert(face,size=1,intensity=1,aspect_ratio=1.0,ex_move=[0,0],mode='all_face'):

    h,w = face.shape[:2]
    landmark = face_recognition.face_landmarks(face)[0]
    # print(landmark)
    landmark_src = np.array(landmark['chin']+landmark['left_eyebrow']+landmark['right_eyebrow']+\
        landmark['nose_bridge']+landmark['nose_tip']+landmark['left_eye']+landmark['right_eye']+landmark['top_lip']+\
        landmark['bottom_lip'])

    landmark_src = np.concatenate((get_borderpoints(face), landmark_src), axis=0)
    TriangleList_src = delaunay(h,w,landmark_src)
    TriangleList_dst = TriangleList_src.copy()


    nikemouth_landmark = get_nikemouth_landmark(landmark_src,alpha=size,aspect_ratio=aspect_ratio,mode = mode)
    if mode == 'only_mouth':
        for i in range(24):
            move = ex_move+(nikemouth_landmark[i]-landmark_src[56+i])*intensity
            TriangleList_dst = changeTriangleList(TriangleList_dst, landmark_src[56+i],move)
    else:
        for i in range(80-25):
            move = ex_move+(nikemouth_landmark[i]-landmark_src[25+i])*intensity
            TriangleList_dst = changeTriangleList(TriangleList_dst, landmark_src[25+i],move)

    Ms = get_Ms(TriangleList_src,TriangleList_dst)
    masks = get_masks(face, TriangleList_dst)
    face_new = replace_delaunay(face, Ms, masks)

    return face_new

# # draw_delaunay(img, TriangleList, delaunary_color):

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',face_new)
# cv2.waitKey(0)
# cv2.destroyAllWindows()