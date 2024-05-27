# OpenImagery - AI Image Generator

OpenImagery is a powerful AI-based image generation tool that allows users to create stunning images based on text prompts. It leverages advanced AI models and offers a variety of configurations to customize the generated images.

## Features

- **User-Friendly Interface**: Intuitive and easy-to-use GUI built with PyQt6.
- **Customizable Prompts**: Enter detailed prompts and negative prompts to guide the image generation.
- **Model Selection**: Choose from various AI models for different styles and quality.
- **Configurable Parameters**: Adjust CFG scale and steps to control the generation process.
- **Live Logging**: Real-time logging to monitor the status of image generation.
- **Image Display**: View the generated image directly within the application.

## Installation

### Prerequisites

- Python 3.7+
- PyQt6
- Requests

### Clone the Repository

```bash
git clone https://github.com/spidirman/OpenImagery.git
cd OpenImagery
```

### Install Dependencies

```bash
pip install pyqt6 requests
```

## Usage

### Running the Application

```bash
python main.py
```
or use the executable file


### User Guide

1. **Enter your prompt**: Type the description of the image you want to generate.
2. **Negative Prompt**: Specify elements you want to avoid in the image. A default negative prompt is provided.
3. **CFG Scale**: Enter the CFG scale value (default: 7). This value controls how closely the model follows the prompt.
4. **Steps**: Set the number of steps for the image generation process (default: 30). More steps typically result in higher quality images.
5. **Sampler and Model**: Choose from available samplers and models to customize the generation process.
6. **Generate Image**: Click the "Generate Image" button to start the image generation. Logs will be displayed in real-time.
7. **View Image**: The generated image will be displayed once the process is complete.

### Example Configuration

- **Prompt**: "A beautiful landscape with mountains and a river."
- **Negative Prompt** (optional): "disfigured, low quality, cropped"
- **CFG Scale**: 7
- **Steps**: 30
- **Sampler**: [Choose a sampler from the dropdown]
- **Model**: [Choose a model from the dropdown]

## Development

### Structure

- **main.py**: Main application script.
- **LoadingScreen**: Class for displaying the splash screen.
- **MainApp**: Class for the main application interface.
- **generate_image**: Function for handling image generation requests.

### Contributing

We welcome contributions to enhance OpenImagery. Please fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Thanks
Thanks to SPITFIRE for providing his [api](https://api.sitius.ir/) for free 
