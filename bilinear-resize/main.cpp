#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
using namespace cv;
using namespace std;

Vec3b getscaledvalue(Mat& image, float x, float y) {
    x = max(0.0f, min(x, static_cast<float>(image.cols - 1))); // 0<=x<=cols-1
    y = max(0.0f, min(y, static_cast<float>(image.rows - 1))); // 0<=y<=rows-1

    int x_floor = static_cast<int>(floor(x));
    int y_floor = static_cast<int>(floor(y));
    int x_ceil = static_cast<int>(ceil(x));
    int y_ceil = static_cast<int>(ceil(y));

    float x_diff = x - x_floor;
    float y_diff = y - y_floor;

    Vec3b intensity1 = image.at<Vec3b>(y_floor, x_floor);
    Vec3b intensity2 = image.at<Vec3b>(y_floor, x_ceil);
    Vec3b intensity3 = image.at<Vec3b>(y_ceil, x_floor);
    Vec3b intensity4 = image.at<Vec3b>(y_ceil, x_ceil);

    Vec3b interpolated_value = intensity1 * (1 - x_diff) * (1 - y_diff) + intensity2 * x_diff * (1 - y_diff) + intensity3 * (1 - x_diff) * y_diff + intensity4 * x_diff * y_diff;

    return interpolated_value;
}

int main() {
    //read the picture
    Mat image;
    Mat sign;
    image = imread("tiger.jpeg", IMREAD_COLOR); // Read the file
    sign = imread("sign.jpeg", IMREAD_COLOR); // Read the file
    if (image.empty()) // Check for invalid input
    {
        cout << "Could not open or find the image" << endl;
        return -1;
    }
    if (sign.empty()) // Check for invalid input
    {
        cout << "Could not open or find the sign" << endl;
        return -1;
    }

    // Add the signature
    int startX = image.cols - sign.cols;
    int startY = image.rows - sign.rows;
    for (int y = 0; y < sign.rows; y++) {
        for (int x = 0; x < sign.cols; x++) {
            Vec3b intensity = sign.at<Vec3b>(y, x);
            if (intensity != Vec3b(255, 255, 255)) { // delete white
                image.at<Vec3b>(startY + y, startX + x) = intensity;
            }
        }
    }

    // Turn into black and white
    Mat grayscale_image(image.rows, image.cols, CV_8UC1); // Create a blank grayscale image
    for (int i = 0; i < image.rows; i++) {
        for (int j = 0; j < image.cols; j++) {
            Vec3b intensity = image.at<Vec3b>(i, j);
            // calculate the grayscale_value
            int grayscale_value = intensity[0]*0.1 + intensity[1]*0.6 + intensity[2]*0.3;
            grayscale_image.at<uchar>(i, j) = grayscale_value;
        }
    }

    // Resize the picture
    float scale_factor;
    cout << "Enter th scaled range(0.1~2)：";
    cin >> scale_factor;
    Mat scaled_image(image.rows * scale_factor, image.cols * scale_factor, CV_8UC3); // Create a new image
    for (int i = 0; i < scaled_image.rows; i++) {
        for (int j = 0; j < scaled_image.cols; j++) {
            float original_i = i / scale_factor; // calculate the original position
            float original_j = j / scale_factor;
            scaled_image.at<Vec3b>(i, j) = getscaledvalue(image, original_j, original_i); // calculate the pixel position
        }
    }

    //Show all the pictures
    namedWindow("Original Image", WINDOW_AUTOSIZE); // Create a window for display.
    imshow("Original Image", image); // Show our image inside it.
    namedWindow("Grayscale window", WINDOW_AUTOSIZE); // Create a window for display.
    imshow("Grayscale window", grayscale_image); // Show our image inside it.
    namedWindow("Scaled Image", WINDOW_AUTOSIZE); // Create a window for display.
    imshow("Scaled Image", scaled_image); // Show our image inside it.
    waitKey(0); // Wait for a keystroke in the window
    destroyAllWindows();
    return 0;
}
