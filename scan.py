# -*- coding: utf-8 -*-
"""
scan
#https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
"""
import cv2 
import matplotlib.pyplot as  plt
import numpy as np
import imutils

def ScanImage(address):
    image=cv2.imread(address) #이미지 불러오기
    
    orig =image.copy()
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, ksize = (0,0), sigmaX= 1)
    edged=cv2.Canny(im_gray,50,200) #canny edge
    #모폴로지연산 closing으로 틈 제거
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, k)
    
    def order_point(pts):
        rect = np.zeros((4,2),dtype='float32')
        
        s=pts.sum(axis=1)
        rect[0]=pts[np.argmin(s)]
        rect[2]=pts[np.argmax(s)]
        
        diff=np.diff(pts, axis=1)
        rect[1]=pts[np.argmin(diff)]
        rect[3]=pts[np.argmax(diff)]
        
        return rect
    	
    def four_point_transform(image, pts):
        rect=order_point(pts)
        (tl,tr,br,bl)=rect
        
        widthA=np.sqrt(((br[0]-bl[0])**2)+((br[1]-bl[1])**2))
        widthB=np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))
        maxWidth=max(int(widthA),int(widthB))
        
        heightA=np.sqrt(((tr[0]-br[0])**2)+((tr[1]-br[1])**2))
        heightB=np.sqrt(((tl[0]-bl[0])**2)+((tl[1]-bl[1])**2))
        maxHeight=max(int(heightA),int(heightB))
        
        dst=np.array([
            [0,0],
            [maxWidth - 1, 0],
            [maxWidth-1,maxHeight-0],
            [0,maxHeight-1]], dtype="float32")
        M=cv2.getPerspectiveTransform(rect,dst)
        warped=cv2.warpPerspective(image,M,(maxWidth,maxHeight))
        
        return warped
    
    ##가장큰 사각형이 종이라는 가정
    cnts =cv2.findContours(edged.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #RETR_LIST 계층 상관없이 모든 경계선 찾기
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse = True)
    #크기별 정렬
    for c in cnts:
        peri=cv2.arcLength(c,True)
        #arcLength 외곽선 길이 반환
        approx = cv2.approxPolyDP(c,0.02*peri, True)
        #외곽선 근사화/단순화
        if len(approx)==4:
            screenCnt = approx
            break
        #사각형일때 까지 ->가장큰 사각형 영역
    	
    ##변환+전처리
    warped = four_point_transform(orig, screenCnt.reshape(4,2)) #변환/함수참고   
    warped_g=cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    warped_g = cv2.bilateralFilter(warped_g, -1, 50, 3)
    warped_inv=cv2.bitwise_not(warped_g)
    T,_ = cv2.threshold(warped_inv, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _,sample = cv2.threshold(warped_inv, min(180,int(T*1.2)), 255, cv2.THRESH_BINARY )  #bi+ otsu*1.2
    (h, w) = warped.shape[:2]
    h_=int(h*0.9)
    w_=int(w*0.9)
    hh=h-h_
    ww=w-w_
    sample_c=sample[hh:h_,ww:w_].copy() #끝을 잘라낸 이미지
    scan=cv2.bitwise_not(sample) #scan image
    return scan,sample_c

if __name__=='__main__':
    
    #check scan
    scan,sample_c=ScanImage('test/scantest.jpg')
    resize_scan=cv2.resize(scan, (0,0), fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
    
    cv2.imshow('scan',resize_scan)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    plt.subplot(1,2,1)
    plt.imshow(scan, cmap='gray')
    plt.title('scan')
    plt.subplot(1,2,2)
    plt.imshow(sample_c, cmap='gray')
    plt.title('sample_c')
    plt.show()
