> ---
> Title: Tokenization & Sentiment Analysis (By Group "FINIX")
> Date: 2024-03-13 12:01
> Category: Progress Report
> Tags: Group FINIX
> ---
>

# Abstract

This post focuses on tokenization and sentiment analysis. We chose a subset of our datasets, tokenized them with a Huggingface pretrained model, and conducted sentiment analysis to evaluate the tools mentioned in our lecture notes. However, the tools didn't perform as anticipated, leading to some results needing refinement. Thus, we've made adjustments to improve the accuracy on our results.

## Tokenization

> "The basic idea is to split up the whole text document into smaller parts, the so-called tokens. A token can be a single word, but it can also be an n-gram, a sentence, a paragraph, all hashtags (e.g. in a tweet), or you could use it to separate punctuation. Tokenization can be important to get a deeper understanding of words." 

In this section, we explore various methods for tokenizing text. Our initial approach utilized the Natural Language Toolkit (nltk) with regular expressions for the task. However, we found this method to fall short in effectiveness. To improve our results, we then turned to the pretrained model "bert-base-uncased" available through the Huggingface package. We believe it offers a more effective tokenization.

```
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
```

Here is a short example using *Bert* to tokenize the text:

> I'm sure there's a bubble in there, especially right now with NVDA. But much like with the long term there will be a couple kings that will come out of it and significantly shape the direction of our technological advancement.

The tokens:

```
['i', "'", 'm', 'sure', 'there', "'", 's', 'a', 'bubble', 'in', 'there', ',', 'especially', 'right', 'now', 'with', 'n', '##vd', '##a', '.', 'but', 'much', 'like', 'with', 'the', 'long', 'term', 'there', 'will', 'be', 'a', 'couple', 'kings', 'that', 'will', 'come', 'out', 'of', 'it', 'and', 'significantly', 'shape', 'the', 'direction', 'of', 'our', 'technological', 'advancement', '.']
```

As shown in the token list, there are some tokens like ',', 's' and other useless marks. Since the sentiment model will ignore them, so we don't do further cleaning here.  

## Sentiment Analysis

> "Sentiment in general refers to opinions, feelings, and emotions, and in a financial context to optimism and pessimism in financial markets. As such, sentiment is of subjective nature, but it is nonetheless important because it can drive human decision making in finance."

Primarily, we tested the tools mentioned in the lecture notes, and we found that the current packages don't bring us a good results. That's because general-purpose sentiment dictionaries often misclassify common financial terminology. For instance, words that are typically considered negative in everyday language may not carry the same sentiment in a financial context. Therefore, it's important to focus on financial dictionary. 

To achieve this purpose, we decide to use ***LM* (Loughran-McDonald Dictionary)** model from *pysentiment2*. 

```
from pysentiment2_updated import LM # updated pysentiment2 with the lastest version of LM dictionary
score = lm.get_score(tokens)
```

> [!NOTE]
>
> The **Loughran-McDonald Dictionary** is a specialized lexicon developed for analyzing the sentiment in financial documents. It was created by Tim Loughran and Bill McDonald. 

We have updated our Loughran-McDonald dictionaries to the latest version to ensure the accurate capture of sentiments for newly emerging words. Additionally, we've customized the *pysentiment2* library to enhance its functionality, so that  it can reports counts, proportion of total, average proportion per document, standard deviation of proportion per document, document count, words with sentiments(this is the part we add to the source code).

> The sentiment categories are: negative, positive, uncertainty, litigious, strong modal, weak modal, and constraining. **The sentiment words are flagged with a number indicating the year in which they were added to the list. **

Despite updates to the Loughran-McDonald dictionaries, some terms still lack the appropriate sentiment assignment. For instance, we believe "bubble" should be marked negatively, contrary to its neutral classification in the dictionary. To address this, we manually marked "bubble" as negative, which  changed the sentiment score of the analyzed comment to -0.99.
