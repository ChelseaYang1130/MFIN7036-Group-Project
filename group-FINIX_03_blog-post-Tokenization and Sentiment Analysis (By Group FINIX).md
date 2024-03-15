> ---
> Title: Tokenization & Sentiment Analysis (By Group "FINIX")
> Date: 2024-03-18 12:01
> Category: Progress Report
> Tags: Group FINIX

# Abstract

This post focuses on tokenization and sentiment analysis. We chose a subset of our datasets, tokenized them with a Huggingface pretrained model, and conducted sentiment analysis to evaluate the tools mentioned in our lecture notes. However, the tools didn't perform as anticipated, leading to some results needing refinement. Thus, we've made adjustments to improve the accuracy on our results.

## Tokenization

> "The basic idea is to split up the whole text document into smaller parts, the so-called tokens. A token can be a single word, but it can also be an n-gram, a sentence, a paragraph, all hashtags (e.g. in a tweet), or you could use it to separate punctuation. Tokenization can be important to get a deeper understanding of words." 

In this section, we explore various methods for tokenizing text. Our initial approach utilized the Natural Language Toolkit (nltk) with regular expressions for the task. However, we found this method to fall short in effectiveness. For example, we used nltk to tokenize at first. However, the result is not satisfactory.

Below is the example text we use to tokenize:

> I'm sure there's a bubble in there, especially right now with NVDA. But much like with the long term there will be a couple kings that will come out of it and significantly shape the direction of our technological advancement.

nltk:

```
import nltk

t=nltk.regexp_tokenize(text.lower(), '[a-z]+')
stemmer = nltk.PorterStemmer()
t = [stemmer.stem(token) for token in t]
```

The tokens:

```
['i', 'm', 'sure', 'there', 's', 'a', 'bubbl', 'in', 'there', 'especi', 'right', 'now', 'with', 'nvda', 'but', 'much', 'like', 'with', 'the', 'long', 'term', 'there', 'will', 'be', 'a', 'coupl', 'king', 'that', 'will', 'come', 'out', 'of', 'it', 'and', 'significantli', 'shape', 'the', 'direct', 'of', 'our', 'technolog', 'advanc']
```

As it's shown in the result, the nltk can't capture the complete word from the sentence. For example, we want **"couple"**, and nltk only takes the partial word **"coupl"**. Same with **"advanc"**. It's **"advancement"** indeed.

```
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
```

To improve our results, we then turned to the pretrained model "bert-base-uncased" available through the Huggingface package. We believe it offers a more effective tokenization.

Here is a same example using *Bert* to tokenize the text:

```
['i', "'", 'm', 'sure', 'there', "'", 's', 'a', 'bubble', 'in', 'there', ',', 'especially', 'right', 'now', 'with', 'n', '##vd', '##a', '.', 'but', 'much', 'like', 'with', 'the', 'long', 'term', 'there', 'will', 'be', 'a', 'couple', 'kings', 'that', 'will', 'come', 'out', 'of', 'it', 'and', 'significantly', 'shape', 'the', 'direction', 'of', 'our', 'technological', 'advancement', '.']
```

As shown in the token list, there are some tokens like ',', 's' and other useless marks. Since the sentiment model will ignore them, so we don't do further cleaning here.  The partial word problem is also solved here using *Bert.*

## Sentiment Analysis

> "Sentiment in general refers to opinions, feelings, and emotions, and in a financial context to optimism and pessimism in financial markets. As such, sentiment is of subjective nature, but it is nonetheless important because it can drive human decision making in finance."

Primarily, we tested the tools mentioned in the lecture notes, and we found that the current packages don't bring us a good results. That's because general-purpose sentiment dictionaries often misclassify common financial terminology. For instance, words that are typically considered negative in everyday language may not carry the same sentiment in a financial context. Therefore, it's important to focus on financial dictionary. 

To achieve this purpose, we decide to use ***LM* (Loughran-McDonald Dictionary)** model from *pysentiment2*. 

> [!NOTE]
>
> The **Loughran-McDonald Dictionary** is a specialized lexicon developed for analyzing the sentiment in financial documents. It was created by Tim Loughran and Bill McDonald. 

```
from pysentiment2_updated import LM # updated pysentiment2 with the lastest version of LM dictionary
score = lm.get_score(tokens)
```

> [!NOTE]
>
> *Pysentiment2* is a library released in **June 2020** for sentiment analysis in a dictionary framework. Both Harvard IV-4 Dictionary and Loughran-McDonald Dictionariy are provided in the library. During our work, we found that a new version of the LM dictionary was released in Feb 2024. The latest version of the dictionary contains **67** additional financial terminology compared to the built-in version in the pysentiment2 library. We **replaced** the LM.csv file located at pysentiment2-0.1.1\pysentiment2\static to update the LM dictionary version, hoping to obtain more accurate and comprehensive sentiment analysis results.

We have updated our Loughran-McDonald dictionaries to the latest version to ensure the accurate capture of sentiments for newly emerging words. 

Additionally, we've customized the *pysentiment2* library to enhance its functionality, so that  it can reports counts, proportion of total, average proportion per document, standard deviation of proportion per document, document count, words with sentiments(this is the part we add to the source code).

```
def get_score(self, terms):
        """Get score for a list of terms.
        
        :type terms: list
        :param terms: A list of terms to be analyzed.
        
        :returns: dict
        """
        assert isinstance(terms, list) or isinstance(terms, tuple)
        
        pos_words = []
        neg_words = []
        score_li = []
        for term in terms:
            score_li.append(self._get_score(term))
            if term in self._posset:
                pos_words.append(term)
            elif term in self._negset or term in ["fake","bubble"]:
                neg_words.append(term)

    
        score_li = np.asarray(score_li)
        
        s_pos = np.sum(score_li[score_li > 0])
        s_neg = -np.sum(score_li[score_li < 0])
        
        s_pol = (s_pos-s_neg) * 1.0 / ((s_pos+s_neg)+self.EPSILON)
        s_sub = (s_pos+s_neg) * 1.0 / (len(score_li)+self.EPSILON)
        
        return {self.TAG_POS: s_pos,
                self.TAG_NEG: s_neg,
                self.TAG_POL: s_pol,
                self.TAG_SUB: s_sub,
                "Positive words":pos_words,
                "Negative words":neg_words,
                "tokens":terms
                }
```

> The sentiment categories are: negative, positive, uncertainty, litigious, strong modal, weak modal, and constraining. **The sentiment words are flagged with a number indicating the year in which they were added to the list. **

```
        for term in terms:
            score_li.append(self._get_score(term))
            if term in self._posset:
                pos_words.append(term)
            elif term in self._negset or term in ["fake","bubble"]:
                neg_words.append(term)
                
        return {....
                "Positive words":pos_words,
                "Negative words":neg_words,
        		"tokens":terms
        }
```

Above is the exact modifications we made to the source code. Despite updates to the Loughran-McDonald dictionaries, some terms still lack the appropriate sentiment assignment. For instance, we believe "bubble" should be marked negatively, contrary to its neutral classification in the dictionary. To address this, we manually **marked "bubble" as negative**, which  changed the sentiment score of the analyzed comment to -0.99. 

In the code, we add a list `["fake", "bubble"]` which contains all the words that are not in the dictionary but in our views are negative. For the following negative words that are in the dictionary, we add them to the list. We also output the sentimental words in the return part.





