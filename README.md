# HtmlClonesDetector

## Description

HtmlClonesDetector is a program that verifies the similarity between multiple websites through several complex stages!  
The underlying logic is quite interesting:

### Stage 1: Checking HTML and CSS Code

- As the first step, I decided that the best approach is to check the similarity between HTML code using the **html_similarity** library.
- This library compares two sequences in parallel, finds the longest common subsequence, and recursively applies the process to the remaining parts.
- Essentially, it verifies the **HTML** and **CSS** structure.

### Stage 2: Visual Comparison of Websites

Checking the HTML code is not enough because a website may look the same to a user but can be coded in multiple ways.  
Therefore, the best approach is to verify the actual appearance.  

The main idea was to take **screenshots** of websites and compare them to determine their similarity.  
I used two methods:

#### **1. `compare_images_ssim`** (less precise but useful as an indicator)

- Read the images using `cv2`.
- Resize one of them to enable comparison without losses.
- Split the images into **RGB** channels (grayscale could be used, but I decided to keep them in color).
- Compute **SSIM** for each RGB color channel to check similarity.
- Finally, calculate the average using NumPy (`np.mean`).

#### **2. `calculate_feature_similarity`** (precise method)

- Here, I use `VGG16` as the **base_model**—a pre-trained neural network trained on ImageNet to recognize various objects.
- I use **block5_pool**, a feature matrix that represents high-level characteristics of images (shapes, textures, patterns).

##### `preprocess_image` - Image Processing

- Resize the image to **224x224** (input size required by `VGG16`).
- Load the image into a 3D array (`224x224x3`).
- Apply `expand_dims` to create a **batch** of images (`1x224x224x3`).
- Process the images with `preprocess_input`.
- Use `model.predict` to extract visual features.  
  - The output from the `block5_pool` layer has a size of **`1x7x7x512`**.
  - `1` - batch of images, `7x7` - image size in feature space, `512` - number of extracted feature channels.
  - Apply `.flatten()` to transform the 4D matrix into a 1D vector.
- Compute **cosine similarity** between the 1D vectors and return the result.

---

## Main Logic (`check_all`)

- Step by step, compare a website with the others in the vector.
- If the similarity is high, add them to the same list and remove them from the main list.
- Recursively iterate through the array until it is empty.
- First, create the `onlyfiles` list, then call `check_all`.
- Finally, add all lists into a main list and display the result.
- Delete all saved images in **`images/`**.

- PS: All similarity calculation functions return a number between 0 and 1 (indicating how similar they are).

---

## Observations

 **Execution Time**:  
- It may take longer to run due to the costly `take_screenshot` process.  
- Other than that, all other steps execute quickly without issues.  
- Runtime may take aprox 20 minutes !
- The project was built and ran on ARM architecture on MAC OS M1 with 0 errors ! 
---

