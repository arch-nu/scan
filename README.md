scan
=====
convert photo to binary scan image 

## 필요한 모듈  
```python
pip install cv2 
pip install matplotlib.pyplot 
pip install numpy 
pip install imutils
```
## 간단한 설명
종이가 포함된 이미지에서 종이 부분만 찾아서 파일로 저장해준다

## 사용법

1. scan.py실행

2. 주소지정
  * line 92 불러올 이미지파일주소
```python
scan,sample_c=ScanImage('이미지파일주소') 
```

  * line94,95 저장할 파일 위치주소
```python
cv2.imwrite('test/scantest_result.png',scan) #파일저장
cv2.imwrite('test/scantest_result_c.png',sample_c)#파일저장
```
4. 실행결과
 * 파일이 저장된다.  
 * 저장된 파일들의 미리보기를 볼수있다.

## 결과물  
### 입력이미지  
<img src="/test/scantest.jpg" width="60%" height="60%" title="scantest" alt="scantest"></img><br/>
종이전체가 포함된 사진파일이다.

### 출력이미지1 scan  
<img src="/test/scantest_result.png" width="60%" height="60%" title="scantest_result" alt="scantest_result"></img><br/>
종이의 테두리를 따라 사진을 자르고 이진화하였다.  
### 출력이미지2 sample_c    
<img src="/test/scantest_result_c.png" width="60%" height="60%" title="scantest_result_c" alt="scantest_result_c"></img><br/>
추가적인 작업이 용이하게 테두리를 자르고 색상을 반전시켜 영상처리 필요시 간단하게 사용할 수 있도록 전처리가 되어있다.   
### 미리보기
<img src="/test/scantest_result_plot.png" width="70%" height="70%" title="scantest_result_c" alt="scantest_result_c"></img><br/>
matplot의 imshow()를 통해 대략적으로 결과물을 확인할수있다.



#### 참고
https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

