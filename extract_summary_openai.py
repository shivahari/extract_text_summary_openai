#!/usr/bin/env python3

import os
import openai

TEXT = 'Our Active Testing platform seamlessly integrates with existing CI/CD tools and becomes another part of the development workflow. The intended outcome is to provide a way for developers to “shift-left” and make security an early and integral part of the development lifecycle. Ultimately, we want to help customers stop vulnerabilities before they reach production.Software inevitably has bugs, but not all bugs lead to security issues.I recently saw a session by Arista Networks CTO & SVP of Software Engineering Ken Duda on Arista’s Software Quality Journey. During the discussion, he refers to several studies by Jim Gray (Tandem) on software quality and bugs. One study he shares reveals that when engineers initially check in the code, and tell their manager it’s done, there is typically one bug per 10 lines of code. When they then run the code through QA and it gets approved, it typically goes down to one bug per 100 lines of code. After the code finally goes into production, and endures a myriad of maintenance releases over a few years, it then falls to one bug per 1000 lines of code.So the idea is to take out any API security related issues before going into production, and to avoid those few bugs turning into severe security breaches. Not only that, but do it in a way that is much faster than traditionally possible. This entails making the security validation process part of the development process.How it works: Business Logic, not Fuzzing.Active Testing automatically runs more than 100 dynamic tests that simulate malicious traffic, including but certainly not limited to the complete set of OWASP API Top 10. We also leveraged the unique knowledge we gained from having our existing platform in production at numerous customers to simulate those real world attacks in our new testing platform. The developer does not need to be a security expert, but can instead lean on our unique understanding of API security captured in our pre-configured test cases.Active testing can leverage anything that describes your APIs, like an OpenAPI (Swagger) Spec, Postman collection, WSDL, etc. If you don’t have this input, you can also leverage the existing Noname platform to provide that input for Active Testing.developer-velocity-1Now you tell Active Testing how to authenticate against the APIs you want to validate.developer-velocity-2And then you specify which tests out of our bank of tests you want to validate against.developer-velocity-3Active Testing will analyze the business logic of the API to understand how they operate and what their dependencies are. Once we understand this business logic, we can launch API centric attacks against them to validate their security capabilities or lack thereof'

def get_summary(text: str) -> str:
    "Get Summary of a text"

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

if __name__ == '__main__':
    get_summary(TEXT) 
