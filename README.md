# Overview :
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WC_insufficient_result.JPG)


special thanks to prof. Won in Chungnam National University

# What you need
1. Python, Android phone with camera support, 'IP cam' app in its android.
2. Wi-Fi or any Wi-Fi network that supports LAN and is able to connect between PC and portable Android phone camera.

*Make sure that both PC and Android Phone is connected one another in the same Local Area Network and assigned proper Local IP.

# Utilzied Algorithms
Hough Line Transform, Canny Edge, Gaussian Filter,  Line Intersection
HSV range, Dilation & Erosion

This program is designed to locate the weed center from the top view.

# Program execution process
Allocate the file destination to run the program 
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/file%20location.JPG)

![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WC_insufficient_result.JPG)

In python command
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WC_insufficient_monitoring.JPG)

To scrutinize the result Hough line image, you may trigger the button shown "E_RT_Plane" then the program will compute and yield Rho-Theta plane by process. It would take a moment to do so, varing computing capacity.

As a result, its plane shown below. You can check the Hough Line Transform algorithm by evaluating with Rho-Theta plane analysis graph below in Python command
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/Rho-Theta%20plane.JPG)

In Python command
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WC_insufficient_result_HL_RT%20plane.JPG)

Then you notice that "Max value in 2D array is (968,29)", which means that there is a specific point where the highest value assigned in Rho-Theta plane.
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/Rho-Theta%20plane_968_29.JPG)

By changing image process properties:
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WC_sufficient_result.JPG)

In monitoring
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WC_sufficient_monitoring_arithmetic%20mean.JPG)


Additionally, you can recognize multiple weeds with detecting specific HSV range, and the result can be found below with setting properties.
![alt text](https://github.com/Kvasir8/Weed-center-detection-with-Android-camera/blob/master/explanation%20pics/WR_HSV%20range.JPG)
