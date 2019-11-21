
echo "This shell script will install the Anaconda environment required to run sea-lice-forecasting"
echo "Doing this will require the current user to have Anaconda installed"
read -p "Do you want to proceed with the installation? (Y/n)" choice
case "$choice" in
  y|Y ) conda env create -f environment.yml -n sealice-env;; 
  n|N ) echo "Exiting";;
  * ) echo "Exiting";;
esac

