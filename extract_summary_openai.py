#!/usr/bin/env python3

import optparse
import os
import bs4
import nltk
import requests
import openai


def get_summary(text: str) -> str:
    "Get Summary of a text"
    try:
        # remove \n from the text
        text = text.replace('\n', '')

        # add \n to the end of the text
        tldr_tag = "\n tl;dr:"
        text = text + tldr_tag
        print(f"The Input text is {text}")

        # we do not know why this step is needed, need to explore
        engine_list = openai.Engine.list()

        # text summarization
        if os.getenv('OPENAI_API_KEY') is not None and os.getenv('OPENAI_ORGANIZATION') is not None:
            response = openai.Completion.create(engine='davinci',
                                                prompt=text,
                                                temperature=0.3,
                                                max_tokens=140,
                                                top_p=1,
                                                frequency_penalty=0,
                                                presence_penalty=0,
                                                stop=['\n'])
            summary = response["choices"][0]["text"]
            print(f"The summary is: {summary}")
    except openai.error.InvalidRequestError as err:
        # reduce the tokens(words) passed as input
        # This model's maximum context length is 2049 tokens
        # remove the stop words using nltk and try again
        token_words = nltk.tokenize.word_tokenize(text)
        token_words_wo_stop_words = [ word for word in token_words if not word in nltk.corpus.stopwords.words() ]
        text = ' '.join(token_words_wo_stop_words)
        print(f"The Input text with reduced token is {text}")
        response = openai.Completion.create(engine='davinci',
                                            prompt=text,
                                            temperature=0.3,
                                            max_tokens=140,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stop=['\n'])
        summary = response["choices"][0]["text"]
        print(f"The summary is: {summary}")


if __name__ == '__main__':
    parser = optparse.OptionParser()
    usage = "usage: %prog [options]"
    parser.add_option('--url',
                      type='string',
                      help='Blog post URL',
                      dest='url')
    options, arguments = parser.parse_args()

    if options.url:
        response = requests.get(options.url)
        html_page = response.text
        soup = bs4.BeautifulSoup(html_page, 'html.parser')
        text = soup.get_text()
        get_summary(text)
