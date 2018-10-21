#include <opencv2/opencv.hpp>

int main(void)
{
    cv::Mat src_img;
    src_img = cv::imread("../sample.png", 1);
    // 画像が読み込まれなかったらプログラム終了
    if(src_img.empty()) {
        return -1;
    }
    
    // 結果画像表示
    cv::namedWindow("Image", CV_WINDOW_AUTOSIZE|CV_WINDOW_FREERATIO);
    cv::imshow("Image", src_img);
    cv::waitKey(0);

    return 0;
}
