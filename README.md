# Web-based Automated Scorecard Reading and Calculation

This is a UCF senior design project completed by a team
of six from September 2024 - May 2025 and is a practical
application of the knowledge gained from our undergraduate
computer science education.

## Goal

Develop an internet based app tailored to the iPhone that
automates the reading and calculation of score cards for
the South Eastern Distance Riders Association.

## Problem

Distance riding events are competitions in which horse and
rider pairs compete over distances of 25 to 100 miles. The
goal of each rider is to complete the full distance within
an allotted time with a healthy and sound horse. Each event
is split into two or more segments of approximately 10-20
miles. Horses are evaluated on soundness after each segment
and are only allowed to continue to the next segment if
they pass the vet check. These soundness evaluations are
used to determine the final scores.

Two scorecards are typically used: CTR to judge a single
entrant, and BC to judge multiple entrants.

## Solution

A web based app that will allow a user to use their iPhone
to take a photo of a score card, use computer vision/machine
learning techniques to read the written values on the
scorecard, allow the user to review (and correct if needed)
the values read in, and then calculate and display the results.

## Documentation

[React Frontend](./frontend#getting-started-with-create-react-app)

[Express Backend](./backend#expressjs-server)

[Image Processing and Segmentation](./Python/Preprocessing_Package/preprocessing#image-processing-test)

[Optical Character Recognition](./Python/OCR_Package/OCR#ocr-package)

[API Reference](./backend/API.md)

[Environment Variables Reference](./ENV.md)

[Python Setup](./Python#configuring-python)

[TorchServe Setup](./model_server#torchserve-setup-guide)

[Rick's Video](https://www.youtube.com/watch?v=E4WlUXrJgy4)


