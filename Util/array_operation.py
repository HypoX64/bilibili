import numpy as np

def interp(y,length):
    xp = np.linspace(0, len(y)-1,num = len(y))
    fp = y
    x = np.linspace(0, len(y)-1,num = length)
    return np.interp(x, xp, fp)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x));

def pad(data,padding):
    pad_data = np.zeros(padding, dtype=data.dtype)
    data = np.append(data, pad_data)
    return data

def normliaze(data, mode = 'norm', sigma = 0, dtype=np.float32, truncated = 2):
    '''
    mode: norm | std | maxmin | 5_95
    dtype : np.float64,np.float16...
    '''
    data = data.astype(dtype)
    data_calculate = data.copy()
    if mode == 'norm':
        result = (data-np.mean(data_calculate))/sigma
    elif mode == 'std':
        mu = np.mean(data_calculate)
        sigma = np.std(data_calculate)
        result = (data - mu) / sigma
    elif mode == 'maxmin':
        result = (data-np.mean(data_calculate))/(max(np.max(data_calculate),np.abs(np.min(data_calculate))))
    elif mode == '5_95':
        data_sort = np.sort(data_calculate,axis=None)
        th5 = data_sort[int(0.05*len(data_sort))]
        th95 = data_sort[int(0.95*len(data_sort))]
        baseline = (th5+th95)/2
        sigma = (th95-th5)/2
        if sigma == 0:
            sigma = 1e-06
        result = (data-baseline)/sigma

    if truncated > 1:
        result = np.clip(result, (-truncated), (truncated))

    return result.astype(dtype)

def diff1d(indata,stride=1,padding=1,bias=False):

    pad = np.zeros(padding)
    indata = np.append(indata, pad)
    if bias:
        if np.min(indata)<0:
            indata = indata - np.min(indata)

    outdata = np.zeros(int(len(indata)/stride)-1)
    for i in range(int(len(indata)/stride)-1):
        outdata[i]=indata[i*stride+stride]-indata[i*stride]
    return outdata


def findpeak(indata, ismax=False, interval=10, threshold=0.1, reverse=False):
    '''
    return:indexs
    '''
    indexs = []
    if reverse:
        indata = -1*indata
        indexs = [0,len(indata)-1]
    else:
        indata = np.clip(indata, np.max(indata)*threshold, np.max(indata))
    diff = diff1d(indata)
    if ismax:
        return np.array([np.argmax(indata)])

    rise = True
    if diff[0] <=0:
        rise = False
    for i in range(len(diff)):
        if rise==True and diff[i]<=0:
            index = i
            ok_flag = True
            for x in range(interval):
                if indata[np.clip(index-x,0,len(indata)-1)]>indata[index] or indata[np.clip(index+x,0,len(indata)-1)]>indata[index]:
                    ok_flag = False
            if ok_flag:
                indexs.append(index)

        if diff[i] <=0:
            rise = False
        else:
            rise = True

    return np.sort(np.array(indexs))

def crop(data,indexs,size):
    if len(data) < size:
        data = pad(data, size-len(data))

    crop_result = []
    for index in indexs:
        if index-int(size/2)<0:
            crop_result.append(data[0:size])
        elif index+int(size/2)<0:
            crop_result.append(data[len(data)-size:len(data)])
        else:
            crop_result.append(data[index-int(size/2):index+int(size/2)])
    return np.array(crop_result)

def cropbyindex(data,indexs,reverse_indexs):
    crop_result = []
    crop_index = []
    for index in indexs:
        for i in range(len(reverse_indexs)-1):
            if reverse_indexs[i] < index:
                if reverse_indexs[i+1] > index:
                    crop_result.append(data[reverse_indexs[i]:reverse_indexs[i+1]])
                    crop_index.append([reverse_indexs[i],reverse_indexs[i+1]])
    return np.array(crop_result),np.array(crop_index)

def get_crossing(line1,line2):
    cross_pos = []
    dif = line1-line2
    flag = 1
    if dif[0]<0:
        dif = -dif        
    for i in range(int(len(dif))):
        if flag == 1:
            if dif[i] <= 0:
                cross_pos.append(i)
                flag = 0
        else:
            if dif[i] >= 0:
                cross_pos.append(i)
                flag = 1
    return cross_pos

def get_y(indexs,fun):
    y = []
    for index in indexs:
        y.append(fun[index])
    return np.array(y)

def fillnone(arr_in,flag,num = 7):
    arr = arr_in.copy()
    index = np.linspace(0,len(arr)-1,len(arr),dtype='int')
    cnt = 0
    for i in range(2,len(arr)-2):
        if arr[i] != flag:
            arr[i] = arr[i]
            if cnt != 0:
                if cnt <= num*2:
                    arr[i-cnt:round(i-cnt/2)] = arr[i-cnt-1-2]
                    arr[round(i-cnt/2):i] = arr[i+2]
                    index[i-cnt:round(i-cnt/2)] = i-cnt-1-2
                    index[round(i-cnt/2):i] = i+2
                else:
                    arr[i-cnt:i-cnt+num] = arr[i-cnt-1-2]
                    arr[i-num:i] = arr[i+2] 
                    index[i-cnt:i-cnt+num] = i-cnt-1-2
                    index[i-num:i] = i+2
                cnt = 0
        else:
            cnt += 1
    return arr,index


def closest(a,array):
    '''
    return:index
    '''

    corrcoefs = []
    for i in range(len(array)):
        #corrcoefs.append(np.linalg.norm(a-array[i], ord=1))
        corrcoefs.append(np.corrcoef(a,array[i])[0][1])
    return corrcoefs.index(np.max(corrcoefs))

def match(src,dst):
    '''
    return:dstindexs
    '''
    indexs = []
    for i in range(len(src)):
        indexs.append(closest(src[i], dst))
    return np.array(indexs)



def main():
    a = [0,2,4,6,8,10]
    print(interp(a, 6))
if __name__ == '__main__':
    main()