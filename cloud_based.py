import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO

# Your Hugging Face API token
HF_TOKEN = "Your_Hugging_API"

# Function to generate the image based on user input
def generate_image():
    prompt = text_input.get()
    if not prompt:
        messagebox.showwarning("Input Error", "Please enter a prompt for the AI to draw.")
        return

    try:
        print("Generating image...")
        # Send request to Hugging Face API
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": prompt}
        response = requests.post("https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
                                 headers=headers, json=payload)

        # Check if the response is successful
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(BytesIO(image_data))

            # Ask the user to select the location to save the image
            output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png")],
                                                       title="Save the generated image")
            if output_path:
                image.save(output_path)
                print(f"Image saved to {output_path}")

                # Display the generated image in the GUI
                display_image(image)
        else:
            print(f"Error generating image: {response.status_code} {response.text}")
            messagebox.showerror("Error", f"Could not generate image: {response.text}")

    except Exception as e:
        print(f"Error generating image: {e}")
        messagebox.showerror("Error", f"Could not generate image: {e}")

# Function to display the image in the GUI
def display_image(image):
    # Convert the image to a format that Tkinter can display
    img_tk = ImageTk.PhotoImage(image)
    img_label.config(image=img_tk)
    img_label.image = img_tk

# Initialize the GUI
root = tk.Tk()
root.title("AI Image Generator")
root.geometry("500x500")

# Prompt label and text entry field
tk.Label(root, text="Enter a prompt for the AI to draw:").pack(pady=5)
text_input = tk.Entry(root, width=50)
text_input.pack(pady=5)

# Button to generate the image
generate_button = tk.Button(root, text="Generate Image", command=generate_image)
generate_button.pack(pady=0)

# Button to generate the image
generate_button = tk.Button(root, text="Exit", command=exit)
generate_button.pack(pady=0)

# Label to display the generated image
img_label = tk.Label(root)
img_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
