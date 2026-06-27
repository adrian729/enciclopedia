# Appendix A: Machine Learning

## Table of Contents

- [1. What Machine Learning Is](#1-what-machine-learning-is)
- [2. Learning from Data: Tasks and Features](#2-learning-from-data-tasks-and-features)
- [3. A Toy Example: Kiki vs. Bouba](#3-a-toy-example-kiki-vs-bouba)
- [4. Types of ML Algorithms](#4-types-of-ml-algorithms)
- [5. Fundamental Problems](#5-fundamental-problems)
- [6. ML Applied to Music](#6-ml-applied-to-music)

## 1. What Machine Learning Is

- **Machine learning (ML)** — a branch of *artificial intelligence* (AI) studying how computers learn to perform tasks by leveraging data, useful where data is plentiful (spam detection, face location, speech recognition, autonomous vehicles)
- **Algorithm vs. ML** — an ordinary *algorithm* specifies actions from input and state via manually written IF-THEN rules (a vending machine); this fails when inputs vary enormously (speech recognition across speakers, environments, microphones) and rules cannot be formally specified
- **Learning from data** — instead of hand-coded rules, an ML algorithm processes a *training data set* many times and tunes its internal machinery to improve inferences (e.g. pairing audio recordings with their spoken text)
- **Performance is measured numerically** — by error rate, accuracy, precision, false-positive rate, or mean squared error; as a rule of thumb, more representative data yields better performance
- **No domain expertise required** — ML shifts engineering effort from writing behavior rules to collecting/labeling data; a web search engine's builders need not be experts in every subject, and the algorithm becomes the *expert* through observing data (with caveats)

## 2. Learning from Data: Tasks and Features

- **Clustering** — organizing a collection by *inferring* how many kinds exist and which examples belong to each; harder because the number of groups must itself be hypothesized
- **Classification** — inferring which already-known kind a given example belongs to; easier than clustering because the categories are known in advance
- **Supervised learning** — the model learns from a data set labeled by humans (classification is an example); the supervision lies in the labeling
- **Unsupervised learning** — the model infers structure from *unlabeled* data (clustering is an example), tuned by objectives like reducing the number of clusters or maximizing distance between them
- **Feature extraction** — rather than feed raw audio (a 60-s CD-quality clip is 5,292,000 16-bit numbers), the waveform is summarized by descriptive *features*: largest/smallest amplitude, mean/variance, *zero-crossing rate*, spectral centroid, spectral flux, harmonicity, pitch, tempo; features may describe whole waveforms or short *frames* (e.g. every 100 ms)
- **Choosing features** — *hand-engineering* uses expert knowledge to define them; *feature selection* computes many and automates the search for the best; *feature learning* folds feature discovery into the pipeline but needs large data. Fewer features need less training data but tend to lower performance — the engineer seeks the smallest set of the best features

## 3. A Toy Example: Kiki vs. Bouba

- **Setup** — two kinds of music, "kiki" and "bouba," with 200 labeled recordings each; build a supervised classifier to tell them apart
- **Train/test split** — the data must be divided so the model is tested on unseen examples: *hold-out* reserves a percentage for testing (here 50%), while *K-fold cross-validation* splits into *K* portions used in turn for testing and training
- **Feature and rule** — using zero-crossing rate per 100 ms frame, a histogram shows "bouba" rarely exceeds 500 crossings; rule: any frame above 500 → "kiki," else "bouba." A *confusion table* on the test set scored all 100 kiki correct and 79/100 bouba correct
- **Raising the threshold to 1000** — yields perfect prediction on full clean recordings, but performance is fragile
- **Fragility** — classifying only a 1-second excerpt misidentifies nearly half the kiki examples; adding white Gaussian noise degrades it (at 42 dB SNR everything is called "kiki")
- **Why it is "machine" learning** — what was done by hand in one dimension (picking a separating threshold from feature distributions), ML does automatically in many dimensions — provided the engineer defines what makes a good decision criterion (large class separation, low prediction error)

## 4. Types of ML Algorithms

- **Nearest neighbor** — the simplest supervised classifier: it assumes each training observation's local neighborhood (e.g. nearest in Euclidean distance) reliably indicates the class of a new observation; *K-nearest neighbor* uses the K closest training points
- **Global-function models** — other supervised algorithms assume observations follow a global function whose parameters are estimated from data (e.g. fitting a line to minimize mean squared error); all supervised methods mix assumptions about local and global structure
- **Clustering algorithms** — unsupervised methods that group observations (e.g. image segmentation by depicted object); *K-means* assigns observations to K engineer-chosen clusters, and *Gaussian mixture models* (GMM) give a probabilistic version
- **Dimensionality reduction** — unsupervised methods separating important features from noise: *principal component analysis* (PCA), *multidimensional scaling*, and the more recent *t-distributed stochastic neighborhood embedding* (tSNE)

## 5. Fundamental Problems

- **Suitcase words** — terms like *learning*, *understanding*, *knowledge*, and *intelligence* pack many meanings that must be unpacked; applying them loosely fosters false expectations. Nearest-neighbor classification is "learning" only in a shallow, nonhuman sense
- **Correlation, not causation** — ML derives power from exploiting correlations in data, not from understanding cause and effect; this fails unexpectedly in complex domains (medical diagnostics, judicial recommendations, finance) and even in music causes harms like recommendation bias, invalid copyright claims, and banal generative output
- **Success does not imply understanding** — high accuracy at reproducing labels does not mean the model learned the underlying concept (Sturm and Wiggins 2021); the kiki classifier learned nothing about "kiki music," and adding an offset to the entire waveform (reducing its zero-crossing rate) would break it entirely
- **Genre-recognition cautionary tale** — over 100 papers studied genre on one 1,000-excerpt data set reporting >80% accuracy; deeper analysis found data flaws (duplicated recordings, repeated artists), and accounting for them dropped accuracy to 40–50% — in one case the system decided based on information below 20 Hz

## 6. ML Applied to Music

- **Sound synthesis and generation** — ML drives neural synthesis and virtual analog modeling; composer Holly Herndon used ML for vocal synthesis alongside human singers
- **Music information retrieval** — ML underlies audio source separation, pitch detection, tempo estimation, music segmentation, semantic tagging, and automatic transcription
- **Gesture recognition** — tools like *Wekinator* translate body gestures into interactive-system control without coding (Fiebrink and Cook 2010)
- **Algorithmic composition and style transfer** — *style transfer* generates music maximizing *content similarity* to an initial score and *style similarity* to a reference (e.g. rendering a J. S. Bach piece in the style of Duke Ellington); Cella (2020) questions obtaining good results without gaining musical knowledge — what is the musical relevance of the learned features?
