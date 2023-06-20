# Install dependencies

<!-- pip3 install opencv-python 
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-testv
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update -->

python -m pip install --upgrade pip
pip install tensorflow
pip install numpy
pip install opencv-python 
pip install easyocr

# Configure
Copy your detect.tflite model into the same repository 
Update the labels.txt file to represent your labels. 

# Go
Run real time detections using the windows_detect.py script 
'python3 windows_detect.py'
