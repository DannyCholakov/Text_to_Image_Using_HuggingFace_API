import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to load the Stable Diffusion model
def load_model():
    try:
        print("Loading model...")
        # Load the Stable Diffusion model, and make sure it's running on CPU
        pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        pipe = pipe.to("cpu")  # Force the model to run on CPU
        print("Model loaded successfully")
        return pipe
    except Exception as e:
        print(f"Error loading model: {e}")
        messagebox.showerror("Error", f"Could not load the AI model: {e}")
        return None

# Function to generate the image based on user input
# Function to generate the image based on user input
def generate_image():
    prompt = text_input.get()
    if not prompt:
        messagebox.showwarning("Input Error", "Please enter a prompt for the AI to draw.")
        return

    # Check if the model is loaded
    if model is None:
        messagebox.showerror("Model Error", "The AI model is not loaded. Cannot generate image.")
        return

    try:
        print("Generating image...")
        # Generate the image with a specified height and width
        with torch.no_grad():
            image = model(prompt, height=256, width=256).images[0]  # Adjust height and width as needed

        # Ask the user to select the location to save the image
        output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png")],
                                                   title="Save the generated image")
        if output_path:
            image.save(output_path)
            print(f"Image saved to {output_path}")

            # Display the generated image in the GUI
            display_image(image)
    except Exception as e:
        print(f"Error generating image: {e}")
        messagebox.showerror("Error", f"Could not generate image: {e}")

# Function to display the image in the GUI
def display_image(image):
    # Convert the image to a format that Tkinter can display
    img_tk = ImageTk.PhotoImage(image)
    img_label.config(image=img_tk)
    img_label.image = img_tk

# Function to handle file selection for user to save or view generated image
def select_image_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        img = Image.open(filepath)
        display_image(img)

# Initialize the GUI
root = tk.Tk()
root.title("AI Image Generator")
root.geometry("500x500")

# Prompt label and text entry field
tk.Label(root, text="Enter a prompt for the AI to draw:").pack(pady=10)
text_input = tk.Entry(root, width=50)
text_input.pack(pady=10)

# Button to generate the image
generate_button = tk.Button(root, text="Generate Image", command=generate_image)
generate_button.pack(pady=20)

# Label to display the generated image
img_label = tk.Label(root)
img_label.pack(pady=20)

# Desktop path for saving generated image
desktop_path = filedialog.askdirectory(title="Select Desktop Location")

# Load the AI model
model = load_model()

# Start the Tkinter event loop
root.mainloop()
