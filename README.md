# sea-lice-forecasting

## Tristan Garry's code accompanying his EEB498 undergraduate honours thesis - It's raining sea lice: forecasting sea lice occurence in juvenile wild salmon

The aim of this project is to accurately forecast within-season occurence of sea lice on wild salmon in the Broughton Archipelago. 

This project aims to use deep learning methods to bring together data including wild salmon parasite counts, temperature data, and farmed salmon data.

Please refer all questions to me at tristan.garry@mail.utoronto.ca

## Work to do

* Write virtual environment helper shell scripts to set this up for those that want to run this code
  * If you want to try to set this up yourself before I write this, here are some starting points:
    * Python - 3.6
    * Tensorflow - 1.13.2
    * Keras - 2.3.1
* Finalise deep learning model to use
* Add baseline models (ARIMA, naive bayes, avg)
* Non-hackily form the input tensors
  * Include the farm data in the input tensors (this is not currently implemented because I wasn't happy with my original implementation)
  * Write resampling helper functions to be robust to new data inputs
* Convert code in jupyter notebook to .py and ensure reproducibility
* Long-term - write visualisations 

## Overall project Status: In progress

