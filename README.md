# Prometeo CLI challenge 001
!['Prometeo logo'](https://cdn.prometeoapi.com/static/img/primary%402x.png)
### [**Link to the challenge**](https://joinignitecommunity.com/desafio-cli/)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) 

_____
## **Installation**
___
### **Virtualenv**

As you can notice, you need to have installed virtualenv on your computer.
Just clone the repo and then execute this:
```
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```
**Note:** The step 2 is for linux. Search the way to enter into your virtual enviroment in your os.

if the download was successful then test the CLI with
```
python -m main version  
python -m main --help
```



### **Docker**

First of all, you need to build the docker image
```
docker build -t prometeo ./
```
***Note:*** This may take a while

Then execute this command
```
docker run -it --name prometeo --rm prometeo
```
A bash console will be open (if everything was ok) and it will be something like: 
```
prometeo_user@123456 $ _
```

Then verify with:
```
python main.py version
python main.py --help
```

### **PyPi**

#### Not yet
___
## **Usage**
___
#### **Getting Started**

#### **1.** Setting up:
First of all, you need to have an API KEY from [**Prometeo**](https://prometeoapi.com/)
For now we be will using a test provider, but you can use the bank provider you want (if you have access to an account, of course).

-**API KEY**: STAIRWAY TO HEAVEN

-**Username**:12345

-**Password**:gfdsa

-**Provider**:Test provider

### **2.** Install the CLI
See the previous section and check with:
**Note:**: I didn't test the CLI on Windows, if you have any errors, please use the docker option.

```
python main.py version
python main.py --help
```

### **3.** Initialize your data

Prometeo CLI has different commands for each section (authorization, providers, and API key) but in order to make things easier for the final user, we group all these commands into a single one.  
```
python -m main init
```
##### Example
![Example](https://i.imgur.com/lIgXJ2S.gif)

**Note**:If you made a mistake while copy/pasting the api key, it will throw you an error, because the key is used to get the providers. In this case, you should manually change the API KEY with this command: `python -m main api-key set` or `python -m main api-key set -k [YOUR KEY]`

If everything was ok, you can check the rest of the commands in the sections below

### **Features**

What makes Prometeo CLI different? I am glad you ask.

- #### **Filter Providers by country**

![Filter providers by country](https://i.imgur.com/fTxDkQp.png)

- #### **Filter Providers by name**
**Note:** This is available only when you add a provider as an option in other commands. The CLI will create a list of all the coincidences related to the name you wrote.  Let's see an example

**If you don't add any bank code, a list of all banks you have already session will appear**
![Filter providers by country](https://i.imgur.com/exnOpJ6.gif)

**Then, if you don't remember the code but remember how it starts, you can write it and see the coincidences**

![Filter providers by country](https://i.imgur.com/9NMPSWY.gif)

- #### **Count and reverse order in movements**
 You can set how many accounts/cards movements you want to see and you can specify the order of the output. More info is below.
Let's see an example.

**Chronological order and 8 movements**
![In chronological order](https://i.imgur.com/ecHuq0t.png)

**Reverse Chronological order and 8 movements**
![In reverse chronological order](https://i.imgur.com/Txdp7BV.png)
- #### **Colors in balance**
This is kinda simple if your balance increased or decreased since the last time you checked. Then the console will print color to represent that.
In this example **Test Account 1** increased since the last time. And **Test Account 2** decreased. 
![Color example](https://i.imgur.com/Q3z6DgP.png)
- #### **PDF reports**
 Yep, with Prometeo CLI you can make pdf reports of the movements in your card/account. This is a simple example.
![PDF example](https://i.imgur.com/4qZpKCr.gif)

**Note:** Notice we only wrote one date and still works. That happened because the last date is [NOW] by default.

### **Commands**

#### **NOTE:** Every command has a --help flag, in case you don't know what options, arguments, or flags exist in the command.

Btw: I know maybe is kinda obvious but [OPTIONS] are optionals parameters.

#### -`accounts`
**Get info of your bank accounts 🏦**
- **`accounts [OPTIONS] `**  
    - **-b or --bank** : The code of your bank
#### Example
![Account example](https://i.imgur.com/lPa4nQR.gif)
- **`accounts movements [FIRST_DATA] [LAST_DATE] [OPTIONS]`**
    -Date formats: d-m-Y | Y-m-d | m-d-Y | m/d/Y | d/m/Y | Y/m/d
    -LAST_DATE Is now by default
    - **-b or --bank** : The code of your bank
    - **-c or --count** : Max movements to show
    - **-o or --order** : Reverse chronological order [False by default] 
    - **-f or --filename** : The name of the report file [Not output by default] 
#### -`api-key`
**Get or set your Prometeo API KEY 🔥**
- **`api-key [COMMANDS]`**:
-**`api-key get`**  : Print the saved key
-**`api-key set [OPTIONS]`**  : Set and save a new API-KEY
    - **-k or --key** : Your API-KEY code

#### -`auth`
**Login/logout into your bank account 💻**
- **`auth [COMMANDS]`**:
- **`auth login [OPTIONS]`**  : Login into your bank account. The app will save session data to easy access in other commands.
    - **-u or --user** : Bank username
    - **-p or --pass** : Bank password
    - **-c or --code** : Bank code
**Note:**Only one session per bank
- **`auth logout`**  :   Logout from your bank account. This will delete all the session data.
    - **-c or --code** : Bank code where you want to logout
    - **-a or --all** : Delete all the session data
#### -`cards`
**Get info of your credit card 💳**
- **`cards [OPTIONS] `**  
    - **-b or --bank** : The code of your bank
- **`cards movements [FIRST_DATA] [LAST_DATE] [OPTIONS]`**
    -Date formats: d-m-Y | Y-m-d | m-d-Y | m/d/Y | d/m/Y | Y/m/d
    -LAST_DATE Is now by default
    - **-b or --bank** : The code of your bank
    - **-c or --count** : Max movements to show
    - **-o or --order** : Reverse chronological order [False by default] 
    - **-c or --currency** : The currency code of your credit card [USD by default] 
    - **-f or --filename** : The name of the report file [Not output by default] 
#### -`init`
**This command will initialize your bank data ⭐**
- **`init`** : See an example in **Get started**

#### -`providers`
**Get a list of the bank providers 🗒️**
- **`providers [OPTIONS] `**  
    - **-ct or --country** : Country code to filter the providers. See an example in  the **features** section.


#### -`uninstall`
**This command will delete all the Prometeo saved data 🗑️**
- **`uninstall`** 
