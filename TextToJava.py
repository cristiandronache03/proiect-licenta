import openai
import os
from os import path

openai.api_key = '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'

from gpt import GPT
from gpt import Example


gpt = GPT(engine="ada",
          temperature=0.3,
          max_tokens=100)

gpt.add_example(Example('Create a java function to sort a list and return it',
                        'private static int[] sortList(int[] v){\n'
                             'boolean t=true;\n'
                             'int aux;\n'
                             'while(t){\n'
                                 't=false;\n'
                                 'for(int i = 0; i<v.length-1; i++){\n'
                                     'if(v[i]>v[i+1]){\n'
                                         'aux = v[i];\n'
                                         'v[i] = v[i+1];\n'
                                         'v[i+1] = aux;\n'
                                         't = true;\n'
                                     '}\n'
                                 '}\n'
                             '}\n'
                             'return v;\n'
                         '}'))

gpt.add_example(Example('Declare an array of integers with 15 numbers from 0 to 10 in Java',
                        'int[] v = {1,6,3,8,6,4,5,8,9,3,6,8,10,2,7};'))

gpt.add_example(Example('Create a class named Employee in Java that has age, height and name as atributes and has a constructor for them',
                        'public class Employee{\n'
                            'private int age;\n'
                            'private double height;\n'
                            'private String name;\n'
                            'private Employee(int age, double height, String name){\n'
                                'this.age = age;\n'
                                'this.height = height;\n'
                                'this.name = name;\n'
                            '}\n'
                        '}'))

def generate(text):
    prompt = text
    
    output = gpt.submit_request(prompt)
    output2 = output.choices[0].text
    output2 = output2.split("output:",1)[1]
    return output2
