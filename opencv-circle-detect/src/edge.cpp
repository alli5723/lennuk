#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

using namespace cv;
using namespace std;

int main( int argc, char** argv )
{
   VideoCapture cap(1); //capture the video from web cam

   if ( !cap.isOpened() )  // if not success, exit program
   {
      cout << "Cannot open the web cam" << endl;
      return -1;
   }

   namedWindow("Control", CV_WINDOW_AUTOSIZE); //create a window called "Control"

   int iLowH = 0;
   int iHighH = 50;

   int iLowS = 150; 
   int iHighS = 255;

   int iLowV = 150;
   int iHighV = 255;

   int blurSigma = 2;

   //Create trackbars in "Control" window
   cvCreateTrackbar("LowH", "Control", &iLowH, 179); //Hue (0 - 179)
   //trackbar name char*, window name char*, value int*, count int[max position of slider])
   cvCreateTrackbar("HighH", "Control", &iHighH, 179);

   cvCreateTrackbar("LowS", "Control", &iLowS, 255); //Saturation (0 - 255)
   cvCreateTrackbar("HighS", "Control", &iHighS, 255);

   cvCreateTrackbar("LowV", "Control", &iLowV, 255); //Value (0 - 255)
   cvCreateTrackbar("HighV", "Control", &iHighV, 255);

   cvCreateTrackbar("BlurSigma", "Control", &blurSigma, 50);

   while (true)
   {
      Mat imgOriginal;

      bool bSuccess = cap.read(imgOriginal); // read a new frame from video

      if (!bSuccess) //if not success, break loop
      {
         cout << "Cannot read a frame from video stream" << endl;
         break;
      }

      Mat imgHSV;

      cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV

      Mat imgThresholded;

      inRange(imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded); //Threshold the image

      //morphological opening (remove small objects from the foreground)
      erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) );
      dilate( imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 

      //morphological closing (fill small holes in the foreground)
      dilate( imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 
      erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) );
      
      GaussianBlur( imgThresholded, imgThresholded, Size(9, 9), blurSigma, blurSigma );
      vector<Vec3f> circles;

      HoughCircles( imgThresholded, circles, CV_HOUGH_GRADIENT, 2, imgThresholded.rows/8, 200, 100, 0, 0);
      //pixel extrapolation method(?)
      if (circles.size() > 0) {
         Point center(cvRound(circles[0][0]), cvRound(circles[0][1]));
         int radius = cvRound(circles[0][2]);
			circle( imgOriginal, center, 3, Scalar(0,255,0), -1, 8, 0 );
			// circle outline
			circle( imgOriginal, center, radius, Scalar(0,0,255), 3, 8, 0 );
      }

      imshow("Thresholded Image", imgThresholded); //show the thresholded image
      imshow("Original", imgOriginal); //show the original image

      if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
      {
         cout << "esc key is pressed by user" << endl;
         break; 
      }
   }

   return 0;

}
