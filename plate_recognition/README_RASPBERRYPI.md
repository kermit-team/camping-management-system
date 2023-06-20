# Install dependencies

pip3 install opencv-python 
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-testv
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install python3-tflite-runtime

sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
sudo apt install tesseract-ocr libtesseract-dev libleptonica-dev
sudo apt install python3-opencv
pip install numpy
sudo apt install libopenblas-base libblas-dev m4 cmake cython python3-dev python3-yaml python3-setuptools
wget https://download.pytorch.org/libtorch/nightly/cpu/libtorch-cxx11-abi-shared-with-deps-latest.zip
unzip libtorch-cxx11-abi-shared-with-deps-latest.zip
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
sudo pip install pytesseract


# Configure
Copy your detect.tflite model into the same repository 
Update the labels.txt file to represent your labels. 

# Go
Run real time detections using the raspberrypi_detect.py script 
'python3 raspberrypi_detect.py'