# Example with constant 
Parameterized can be performed by giving different set of encoding files. It can also be performed by adding different parameters to the Control object.
It can be used with  "-c const=?" that will change the value of constant.
---

```json
{
    "encodingsFileList": [
        [
            "encoding.lp"
        ]
    ],
    "controlParameters": [
        [
            "-c const=3"
        ],
        [
            "-c const=2"
        ]
    ],
    "testDescription": [
        {
            "testName": "Model should be exact to number(1),number(2),number(3)",
            "functionName": "exactsetall",
            "arguments" : ["number(1)","number(2)","number(3)"]
        }
    ]
}
```
---
The file "encoding.lp" will be called 2 times ; firstly with the constant *const* equal to 3, and then equal to 2. The unit test is performing a "exactsetall" function that will return "fail" if models are not equal to number(1),number(2),number(3). The encoding will in this case return *[number(1),number(2),number(3)]* and *[number(1),number(2)]*, in the second case, test will fail.
---
Call :

```python
import clintest
ct = clintest.Clintest(['example/constexample/test_encoding.json'])
ct()
```

Output :

```console
Test #1.1  : Model should be exact to number(1),number(2),number(3)
Configuration : {'controlParameters': ['-c const=3'], 'encodingsFileList': ['encoding.lp']}
        Result PASS
Test #1.2  : Model should be exact to number(1),number(2),number(3)
Configuration : {'controlParameters': ['-c const=2'], 'encodingsFileList': ['encoding.lp']}
        Result FAIL
        Additionnal informations : 
    -   Missing (-)/Not desired (+) symbol(s) on model 0 : 
                (-) number(3) 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Test executed in 7.43865966796875e-05 ms
Result on call : Fail
- - - - - - - - - - - -
```