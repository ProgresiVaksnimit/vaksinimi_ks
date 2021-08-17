# Vaccination Progress in Kosovo

This code will send Tweet in [@VaksinimiKS](https://twitter.com/VaksinimiKS) Twitter account containing vaccination progress using a progress bar (inspired by [@year_progress](https://twitter.com/year_progress)) and percentage. The whole idea is based on German Vaccination Progress Twitter Bot -> https://github.com/imbstt/impf-progress-bot

Ex. of Tweet:
```
▓▓▓░░░░░░░░░░░░ 20,9% - të vaksinuar me dozën e parë
▓▓░░░░░░░░░░░░░ 11,3% - të vaksinuar 
Data: 15/08/2021 23:23:58
```

## Script Setup

- Create an app at the [Twitter Developer site](https://developer.twitter.com/) and create app tokens and keys
- Edit [twitter.cfg](./twitter.cfg) and put in your Twitter Consumer and Access tokens/keys
- Change `DRY_RUN = True` in [tw_bot.py](./tw_bot.py) to `False` when you are done testing
- Install needed libraries using requirements file

```
# Create venv
py -3 venv venv

# Activate venv: Linux / MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

The script can now simply be called like this:

```
python tw_bot.py
# or
py -3 tw_bot.py
```

## Deploying

You can deploy the bot in AWS as a Lambda serverless function and trigger it using CloudWatch Event cron-like scheduler using SAM (Serverless Application Model - more: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html). 
Prerequisites:
- AWS Account
- sam installed
- IAM User
- S3 Bucket (where artefacts will be uploaded)

To do so:
```
# Clone the repo
1. git clone https://github.com/ProgresiVaksnimit/vaksinimi_ks.git
2. cd vaksinimi_ks 
# edit twitter.config file by adding your twitter api keys
# inside of template.yaml file, edit Schedule property and set it based on your need
# switch DRY_RUN to False
3. sam build && sam deploy --stack-name [STACK_NAME] --s3-bucket [BUCKET_NAME] --capabilities CAPABILITY_IAM

Note: if it fails to be build because of python version incompatibilites, just edit:
Runtime: python3.7 to Runtime: python[YOUR_VERSION] -> in template.yaml
```

## Data Source

Script will use pull vaccination data from Official Website of Ministry of Health in Republic of Kosovo - [Covid-19 Stats](https://msh.rks-gov.net/sq/statistikat-covid-19) 

## License

MIT
