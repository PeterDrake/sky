# sky
Applying machine learning to sky images to classify (meteorological) clouds.
                                                    
Programs to run:

preprocess.py preprocesses the data

condition-generator.py generates conditions.txt, which describes experimental
    conditions

train.py trains the network

On Coeus, launch.sh calls run.sh to run a set of experiments

show_output.py shows the network's output for a particular image

show_kernels.py shows the kernels in the first convolutional layer

analyze.py finds the images for which the network does worst and displays
    how they disagree with the targets

plot_learning_curve.py plots a learning curve
