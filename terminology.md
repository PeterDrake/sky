# Terminology

This file defines various terms used throughout our code.

## Instruments

- **TSI** Total Sky Imager, which takes a photo of the sky every 30 seconds.
- **ARSCL** Active Remote Sensing of CLoud boundaries, which includes a ceilometer, a micropulsed lidar, and a radar,
all pencil beams pointing straight up.

## Image Files

- **Photo** The photo of the sky, taken every 30 seconds. Called "sky image" in the ARM data.
- **TSI mask** Output of the TSI segmentation algorithm, classifying pixels into clear, thin cloud, etc.
Called "cloud mask" in the ARM data.
- **Network mask** Corresponding output of the neural network.

Note that neither of these are bit masks, as there are more than two categories.

## Scalar Values

- **CF** Cloud fraction from ceilometer. This is the fraction of *time* that there is cloud directly above the ceilometer.
This is typically taken over a 30-minute interval to compensate for the TSI's wider field of view.
- **TSI FSC** Fractional sky cover from TSI mask. This is the fraction of the *sky* that is cloudy (as opposed to clear).
This is typically averaged over all TSI maks in a 15-minute interval. Both thick and thin cloud pixels are counted as cloudy.
- **Network FSC** Fractional sky cover from the network mask.

## Miscellaneous Terms

- **Timestamp** A timestamp of a photo (and therefore its corresponding mask). It is stored as a string in the format
YYYYMMDDhhmmss.

## Data Categories

We have .csv files which provide data for each timestamp, including TSI FSC and CF. The fsc_thin_z column gives the
TSI FSC for thin cloud within +/-50 degrees of the zenith. Based on 15-minute averages of this column, we classify each
timestamp as *typical* or *dubious*.

- **Typical** These have averages < 0.3. We are more confident in the accuracy of the TSI mask on these images, as
they are known to contain shallow cumulus clouds, which are rarely accompanied by thin clouds. These are identified in
the csv.
- **Dubious** These have averages >= 0.3. Since this is unlikely to reflect physical reality, we suspect that the
TSI has improperly labeled many pixels as thin cloud when they are actually, e.g., sun glare.

