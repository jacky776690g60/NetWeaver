![cover](samples/cover.png)

<h1 style="color: white; background: linear-gradient(43deg, #4158D0 0%, #d253c3 58%, #FB5959 100%); text-align: center; padding: 10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; border-radius: 5px; text-transform: capitalize;">
  Net Weaver
</h1>

Built upon Selenium, this suite of tools aims to achieve easier automations for web testing. It simplifies the collection and formatting of references for uses including prompt engineering, picture references gathering, instagram scrapping, etc.

*If you are reading this, you are probably reading the <a href="https://github.com/jacky776690g60/NetWeaver" target="_blank">temporary public repo</a> (used for showcasing what the enxtension can do)*

> <h2 id='toc0'>Table of Content</h2>

1. <a href='#install'>Installation</a>
2. <a href='#folder_structure'>Folder Structure</a>
3. <a href='#run_test'>Run Test</a>
4. [Applications](apps/README.md)
5. <a href='#usage'>Usage</a>

<h1 id="install" style="font-weight: 600; text-transform: capitalize; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #F4B400;">Installation</h1>
<a href='#toc0' style='background: #toc000; margin:0 auto; padding: 5px; border-radius: 5px;'>Back to ToC</a><br><br>

1. `git clone --recurse-submodules https://github.com/jacky776690g60/NetWeaver.git` clone the repo first.
2. (Optional) Create a Python virtual environment and activate it.
   1. `python3 -m venv nwvenv`
   2. activate
      1. `source nwvenv/bin/activate` on mac
3. `pip install -r requirements.txt`
4. (Optional) <a href='#run_test'>Run Test</a> to see if package is working.

### **Additional Downloads**

For certain applications, you may need to download matching test drivers and test browsers first. 

- For Chrome (driver / browser)
   - <a href='https://chromedriver.storage.googleapis.com/'>Selenium Autodownload References</a>
   - <a href='https://googlechromelabs.github.io/chrome-for-testing/'>Chrome Lab (for testing)</a>
     - <a href='https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'>Known Good Versions</a>

<h1 id="folder_structure" style="font-weight: 600; text-transform: capitalize; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #EA638C;">Folder Structure</h1>
<a href='#toc0' style='background: #toc000; margin:0 auto; padding: 5px; border-radius: 5px;'>Back to ToC</a><br><br>

```
/NetWeaver   <- root folder
|-- apps/    <- useful applications you can run
|   ...
|-- config/  <- config your .jsonc files to store information
|   ...
|-- netweaver/ <- main package if you want to use this in other project
|   ...
...
|-- tests/      <- test scripts
|   ...
|-- .gitignore
|-- .gitmodules
|-- README.md
|-- requirements.txt
```


<h1 id="run_test" style="font-weight: 600; text-transform: capitalize; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #EA638C;">Run Test</h1>
<a href='#toc0' style='background: #toc000; margin:0 auto; padding: 5px; border-radius: 5px;'>Back to ToC</a><br><br>

Run test scripts first to see if you have install the necessary packages correctly.

- Run **single test** script

  `python3 -m unittest tests.test_netweaver`

- Run **all tests** together

  `python3 -m tests.entry`



<h1 id="usage" style="font-weight: 700; text-transform: capitalize; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #EA638C;">&#9698; Usage</h1>
<a href='#toc0' style='background: #toc000; margin:0 auto; padding: 5px; border-radius: 5px;'>Back to ToC</a><br><br>

There are two main classes currently:
1. The class `NetWeaver()`
2. Created `EnhancedWebElement`

The intellisens will allow you to shorten the development time of using Selenium functions. 