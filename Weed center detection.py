from __future__ import print_function
import cv2
import numpy as np
import time
import Kmeans
import urllib
import Algorithms as AG
import matplotlib.pyplot as plt

MV = ''
fn = ''
fn_flag = 0
E_UGV = 0
ISM = 0
H = 0
url = ""

def update(*arg):
    global MV
    global fn
    global E_UGV
    global fn_flag
    global ISM
    global H
    global url
    
    if(E_UGV == 1):
        url = input("Input webcam url address from android's camera : \n eg) http://192.168.1.83:8080/shot.jpg \n")
        #url='http://192.168.1.83:8080/shot.jpg'
        
        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        src=cv2.imdecode(imgNp,-1)
        
    elif(fn_flag == 1):
        src = cv2.imread(fn)
    
    elif(fn_flag == 0):
        fn = input("Input image file including extension to test the program : \n eg) img/D7.jpg \n Press 'Q' to exit the current program. \n")
        fn_flag = 1
        src = cv2.imread(fn)
        
        
    start = time.time() #start Image process time counting..
    
    E_Km = cv2.getTrackbarPos('E_Km', 'Enable_fun')
    E_WD4D = cv2.getTrackbarPos('E_WD4D', 'Enable_fun')
    E_WC = cv2.getTrackbarPos('E_WC', 'Enable_fun')
    E_RT_plan = cv2.getTrackbarPos('E_RT_plan', 'Enable_fun')
    
    Resize = cv2.getTrackbarPos('Resize', 'control')
    h0 = cv2.getTrackbarPos('h min', 'control')
    h1 = cv2.getTrackbarPos('h max', 'control')
    s0 = cv2.getTrackbarPos('s min', 'control')
    s1 = cv2.getTrackbarPos('s max', 'control')
    v0 = cv2.getTrackbarPos('v min', 'control')
    v1 = cv2.getTrackbarPos('v max', 'control')
    CAMin = cv2.getTrackbarPos('Con_Area min', 'control') #Counter area from min to max
    CAMax = cv2.getTrackbarPos('Con_Area max', 'control')
    DET_offset = cv2.getTrackbarPos('DET_offset', 'control')
    GB = cv2.getTrackbarPos('HL_Gaussian_blur', 'control')
    TH = cv2.getTrackbarPos('HL_Threshold', 'control')
    THR1 = cv2.getTrackbarPos('Canny_Thres1', 'control')
    THR2 = cv2.getTrackbarPos('Canny_Thres2', 'control')
    
    src = cv2.resize(src, None, fx=(Resize / 10), fy=(Resize / 10), interpolation=cv2.INTER_CUBIC) #resizing image
        
    IHeight, IWidth, _ = src.shape #assigning image info
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    
    print ("---------------------------------")
    print("resized image shape:", src.shape)
        
        
    lower = np.array((h0,s0,v0))
    upper = np.array((h1,s1,v1))
    mask = cv2.inRange(hsv, lower, upper)
        
        
    filtered_E = AG.filter_E(mask)
    filtered_ED = AG.filter_ED(mask)
    filtered_EDG = AG.filter_EDG(mask)
        
    img_result = cv2.bitwise_and(src, src, mask = mask)
    
    '''K-means'''
    if(E_Km == 1):
        Km = mask
        Km[Km == 255] = 1
        Km = np.transpose(np.nonzero(Km))
        Kmeans.Result(Km, 3, 10)
        
    '''Contours'''
    ret, contours, hierarchy = cv2.findContours(filtered_EDG, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Listing Hierarchy structures of contours and generating coordinates for recognized shapes
    total_contours = len(contours) #Total amount of recognized weeds
    result = src.copy()
        
    total_area = 0
    contours_error = []
    contours_ok=[]
    W_area=[]
    W_area_argmax = 0
    W_Compare_Area = []
    WeedNumber = 0
    MV = ""
    DET = 0
    font = cv2.FONT_HERSHEY_SIMPLEX #font assignment
    
    for cnt in contours:
        WeedNumber += 1
        area = cv2.contourArea(cnt)
        total_area += area
        if (area > CAMin and area < CAMax):
            W_Compare_Area.append(area)
            print ("Weed #" + str(WeedNumber) + " area : " + str(area))
            W_area.append(area)
            contours_ok.append(cnt)
        else:
            print ("ERROR AREA: ", area)
            contours_error.append(cnt)

    if len(W_area) > 0:
        W_area_argmax = np.argmax(W_area) + 1
        print("Weed_area_list : ", W_area)
        print("Weed_argmax : Weed #", W_area_argmax)
         
    if len(contours) > 0:
        media = total_area/len(contours)
        print ("\tAREA MEDIA : %.2f" %media)  # average area of calculated weeds, including error area
        #도출된 area값 들의 평균 area '{:.2f}'.format(Tr_cost)
    
    DET_L = -50 - DET_offset
    DET_R = 50 + DET_offset
    
    
    '''Hough Line Transform'''
    if(E_WC == 1):
        
        if(E_RT_plan == 1):
            H = AG.RT_plane(src, GB, THR1, THR2)
            H_1D = H.ravel() #2D image arrays into flatten 1D array
            cv2.imshow('Gray', AG.RT_plane.gray)
            cv2.imshow('Rho-Theta', H)
            plt.imshow( H )
            print("Max value in 2D array : " + str(np.unravel_index(H_1D.argmax(), H.shape)))
            
            
            print("Its value : " + str(np.max(H)))
            
            
        result = AG.HL_IS(src, GB, TH , 1, THR1, THR2)
        
        
        ISM = AG.HL_IS.ISM
        print( "ISM : " + str(ISM) )


    '''Draw contours'''
    WeedNumber = 0 #Reassignment for counting weed numbers again.
    for crc in contours_ok:
        WeedNumber += 1
        print("Weed #%d" %WeedNumber)
        #print("area : ", contours_ok[WeedNumber])
        (x,y), radius = cv2.minEnclosingCircle(crc)
        center = (int(x),int(y))
        DET = int(x) - IWidth//2
        
        if( (W_area_argmax == WeedNumber) ):
            #면적이 가장 큰 민들레 꽃의 순서와 맞으면 분기
            
            #Module이 왼쪽/오른쪽으로 갈지 계산하기 위한 x축 계산변수
            if DET_L<DET & DET<DET_R: #Moving Forward if weed is located in center
                if (MV == 'g') or (MV ==''):
                    MV = 's' #Scanning front distance of UGV from itself to Weed
                    
                else:
                    MV = 'g'
                    
                if(E_UGV == 1):
                    print("UGV command : " + MV)
                    
                #cv2.waitKey(100) #500ms delay
            elif DET_L>DET: MV = 'l'
            elif DET>DET_R: MV = 'r'
                
            print("UGV command : " + MV)
            
        
        radius = int(radius)
        Dis = AG.calculateDistance(IWidth//2, IHeight//2, int(x),int(y))
        
        '''Enable Weed Center for Driving'''
        if(E_WD4D == 1):
            cv2.circle(result, center, radius, (0,250,0), 2) #Weed Center's point drawn
            cv2.circle(result, center, 3, (250, 0, 250), 2)
            cv2.line(result, (IWidth//2, IHeight//2), center, (255, 0, 0), 2)
            cv2.putText(result, 'Weed#%d, Dis : %d' %(WeedNumber, Dis), (int(x),int(y)), font, 0.4, (255,255,255), 1, cv2.LINE_AA)
            
            print ("Center coordinate : ", center)
            print ("Distance from center : %d" %Dis)
            print ("Weed x axis distance from screen : %d" %DET) #인식된 잡초의 x축이 화면중앙의 x축 중심으로부터 벗어난 크기
            
    '''Process ending time'''
    stop = time.time()
    diff = stop - start # 이미지 처리에 총 걸린 시간
    #HSV update 창을 열은 start 시간을 contour작업을 
    #완료한 시간(이미지 1장 처리 = 1 epoch당 걸리는 시간을 diff 변수에 값 할당)을 뺀 것=diff
    t = str("%.3f" % diff)
	#fps = str(int(1//diff))
	#text = "t["+t+"] fps:["+fps+"] AREAS:["+str(len(contours_ok))+"]" + "Movement:["+ MV +"]"
    if(E_WC == 1):
        text = "t["+t+"] AREAS:["+str(len(contours_ok))+"] " + "Center: "+ str(ISM)
    else:
        text = "t["+t+"] AREAS:["+str(len(contours_ok))+"]"
    #Total amount of work time for image process
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(result,text,(15,30), font, .5, (255, 255, 255), 2)
    #font assignment for result
    
    
	#show
    print ("\tTOTAL: ",total_contours)
    print ("\tOK: ", len(contours_ok))
    print ("\tERRORS: ", len(contours_error))
    #잡초로 인식한 contour처리 영역이 일정 영역보다 커서 error가 나면 그 error가 난 형체가 몇 개인지 알려줌.
    
    cv2.imshow('original', src)
    if(E_WD4D == 1):
        cv2.imshow('mask', mask)
        cv2.imshow('filter_Erosion: ', filtered_E)
        cv2.imshow('filter_Erosion + Dilation: ', filtered_ED)
        cv2.imshow('filter_Erosion + Dilation + Gaussian_blur: ', filtered_EDG)
        cv2.imshow('result', result)
        cv2.imshow('Bitwise_and', img_result)
    if(E_WC == 1):
        cv2.imshow('Canny', AG.HL_IS.Canny) #Calling HL attribute of function in AG file 
        
        

def main():
    global E_UGV
    cv2.namedWindow('Enable_fun', 0)
    cv2.createTrackbar('E_UGV', 'Enable_fun', 0, 1, update)  #Enable executing real time weed's center detection with Android camera
    cv2.createTrackbar('E_WD4D', 'Enable_fun', 0, 1, update) #Enable Weed Detection for Driving
    cv2.createTrackbar('E_WC', 'Enable_fun', 0, 1, update)   #Enable Weed Center Detection
    cv2.createTrackbar('E_RT_plan', 'Enable_fun', 0, 1, update)   #Enable Rho-Theta plane for evaluation
    cv2.createTrackbar('E_Km', 'Enable_fun', 0, 1, update)   #Enable K-means (incompleted)
    
    cv2.namedWindow('control', 0)
    cv2.createTrackbar('Resize', 'control', 3, 10, update)
    cv2.createTrackbar('h min', 'control', 20, 179, update)
    cv2.createTrackbar('h max', 'control', 40, 179, update)
    cv2.createTrackbar('s min', 'control', 20, 255, update)
    cv2.createTrackbar('s max', 'control', 255, 255, update)
    cv2.createTrackbar('v min', 'control', 221, 255, update)
    cv2.createTrackbar('v max', 'control', 255, 255, update)
    cv2.createTrackbar('Con_Area min', 'control', 0, 52500, update)
    cv2.createTrackbar('Con_Area max', 'control', 52500, 52500, update)
    cv2.createTrackbar('DET_offset', 'control', 0, 200, update)
    cv2.createTrackbar('HL_Gaussian_blur', 'control', 5, 10, update)
    cv2.createTrackbar('HL_Threshold', 'control', 190, 200, update)
    cv2.createTrackbar('Canny_Thres1', 'control', 50, 200, update)
    cv2.createTrackbar('Canny_Thres2', 'control', 150, 200, update)
    update()
    
    while 1:
        if(E_UGV == 1):
            update()
            if cv2.waitKey(1)&0xFF == ord('q'): #Shutting down the program
                cv2.destroyAllWindows()
                break;
            #cv2.waitKey(100) #100ms delay
            
        if cv2.waitKey(1)&0xFF == ord('q'):
            cv2.destroyAllWindows()
            break;

main()