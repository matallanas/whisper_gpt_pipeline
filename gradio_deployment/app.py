import gradio as gr
import tensorflow as tf
import datasets

'''
We want to create an application that allows the user to select a dataset from a specified list
and pass that with specified parameters to a model to train it on.

Then, we want a way to allow the user to select hyperparameters for their model, train it, and then 
Generate some text! 

'''





def generate_text():
    pass


def train_model():
    pass




# App Construction



demo = gr.Blocks()

with demo:
    gr.Markdown("<h1><center>Generate Text from Youtube with Whisper and GPT!</center></h1>")
    #dataset selector
    with gr.Row():
        with gr.Column():
            ds = gr.Dropdown(["Whispering-GPT/whisper-transcripts-the-verge"])
            #model parameters
            
            epochs = gr.Slider(minimum = 1, maximum = 10, value  = 1, step = 1, interactive = True)
            block_size = gr.Dropdown([32, 64, 128, 256])
            model_checkpoint = gr.Dropdown(["distilgpt2"])
        with gr.Column():
             #train button
            begin_training = gr.Button("Begin Training!")
            #button to generate text iff training done
            create_text = gr.Button("Generate some text!")
    with gr.Row():
        text_output = gr.Textbox(value = "Generated text will appear here")

demo.launch()

