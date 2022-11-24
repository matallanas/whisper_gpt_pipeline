import gradio as gr
from transformers import AutoTokenizer, pipeline

'''
We want to create an application that allows the user to demo the trained models we made
on Youtube dataset!

'''


# TODO
# - Add different decoding mechanisms for generation
# - Text blurb explaining project and motivatoin

# MODEL = ""

# def train_model(dat, model_checkpoint, epochs):
#     # trains model given parameters

#     model = compile_model(model_checkpoint=model_checkpoint)

#     ds = create_dataset(dat, model_checkpoint=model_checkpoint)

#     data_collator = DefaultDataCollator(return_tensors="tf")

#     train_set = ds["train"].to_tf_dataset(
#         columns=["attention_mask", "input_ids", "labels"],
#         shuffle=True,
#         batch_size=16,
#         collate_fn=data_collator,
#     )

#     mod_history = model.fit(train_set, epochs = epochs)
#     MODEl = model

#     return model

def generate_text(model_checkpoint, seed_text, num_return_sequences):
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    p = pipeline("text-generation", model = model_checkpoint, tokenizer = tokenizer)
    genned_text = p(seed_text, num_return_sequences = num_return_sequences)
    genned_text = [x["generated_text"] for x in genned_text]
    return " ".join(genned_text)


# App Construction



demo = gr.Blocks()

with demo:
    gr.Markdown("<h1><center>Generate Text from Youtube with Whisper and GPT!</center></h1>")
    with gr.Row():
        with gr.Column():
            #model parameters
            num_return_seqs = gr.Slider(minimum = 1, maximum = 10, interactive = True, step = 1)
            model_checkpoint = gr.Dropdown(["juancopi81/GPT-Y"], value = "juancopi81/GPT-Y", type = "value")
            seed_text = gr.Textbox("Write some seed text here")
            create_text = gr.Button("Generate some text!")
    with gr.Row():
        text_output = gr.Textbox(value = "Generated text will appear here")
        create_text.click(generate_text, inputs = [model_checkpoint, seed_text, num_return_seqs], outputs=[text_output])

demo.launch()

