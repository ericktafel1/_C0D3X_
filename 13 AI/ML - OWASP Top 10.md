| ID   | Description                                                                                                                                                                           |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ML01 | `Input Manipulation Attack`: Attackers modify input data to cause incorrect or malicious model outputs.                                                                               |
| ML02 | `Data Poisoning Attack`: Attackers inject malicious or misleading data into training data, compromising model performance or creating backdoors.                                      |
| ML03 | `Model Inversion Attack`: Attackers train a separate model to reconstruct inputs from model outputs, potentially revealing sensitive information.                                     |
| ML04 | `Membership Inference Attack`: Attackers analyze model behavior to determine whether data was included in the model's training data set, potentially revealing sensitive information. |
| ML05 | `Model Theft`: Attackers train a separate model from interactions with the original model, thereby stealing intellectual property.                                                    |
| ML06 | `AI Supply Chain Attacks`: Attackers exploit vulnerabilities in any part of the ML supply chain.                                                                                      |
| ML07 | `Transfer Learning Attack`: Attackers manipulate the baseline model that is subsequently fine-tuned by a third-party. This can lead to biased or backdoored models.                   |
| ML08 | `Model Skewing`: Attackers skew the model's behavior for malicious purposes, for instance, by manipulating the training data set.                                                     |
| ML09 | `Output Integrity Attack`: Attackers manipulate a model's output before processing, making it look like the model produced a different output.                                        |
| ML10 | `Model Poisoning`: Attackers manipulate the model's weights, compromising model performance or creating backdoors.                                                                    |

---

### Overpowering

First try to **overpower** the classifier to process more content that is labeled good rather than bad (e.g. ham vs spam). Below shows one spam line followed by ham lines (bee movie script), and tricks the classifier to process the message as ham instead of spam:
```text
Congrats! You are a winner, click here to claim your prize!
According to all known laws of aviation, there is no way a bee should be able to fly.
Its wings are too small to get its fat little body off the ground.
The bee, of course, flies anyway because bees don't care what humans think is impossible.
Yellow, black. Yellow, black. Yellow, black. Yellow, black.
Ooh, black and yellow!
Let's shake it up a little.
Barry! Breakfast is ready!
Coming!
Hang on a second.
Hello?
Barry?

<Rest of the Bee movie script...>
```

### Manipulating the Training Data

We could also upload manipulated training data. The data should trick the classifier into thinking that good is bad and bad is good (or spam is ham and ham is spam). Firstly, reducing the training data from 1,000s of lines to 100 lines makes this easier. Then switch the labels and upload training data to the model:
```text
# Condense training data to 100 lines
# Switch spam and ham labels for ALL lines
spam,Congrats! You are a winner, click here to claim your prize!
ham,According to all known laws of aviation, there is no way a bee should be able to fly.
...
ham,Congrats! You are a winner, click here to claim your prize!
spam,According to all known laws of aviation, there is no way a bee should be able to fly.
```