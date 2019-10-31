import boto3
import time

wafclient = boto3.client('waf-regional', region_name='us-east-1', aws_access_key_id='AKIAS46V6IS5SR2ZVVHM', aws_secret_access_key='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') 
changetoken = wafclient.get_change_token()["ChangeToken"]
print(changetoken)
response = wafclient.create_regex_pattern_set( Name='FileUploadMultiPart', ChangeToken=changetoken )
print(response)
regexpatternct = response["ChangeToken"]
print(regexpatternct)
regextpatternsetid = response["RegexPatternSet"]["RegexPatternSetId"]
changetoken = wafclient.get_change_token()["ChangeToken"]
updateregexresponse = wafclient.update_regex_pattern_set(
                       RegexPatternSetId=regextpatternsetid,
                       Updates=[
                               {
                                   'Action': 'INSERT',
                                   'RegexPatternString': 'multipart/form-data*'
                                },
                           ],
                       ChangeToken=changetoken
                       )
print("Updating Regex pattern Set Done")


changetoken = wafclient.get_change_token()["ChangeToken"]
regexmatchresponse = wafclient.create_regex_match_set(
                        Name='FileUploadMatchCondition',
                        ChangeToken=changetoken
                    )

print("Creating Regex match Set Done")
regexmatchsetid = regexmatchresponse["RegexMatchSet"]["RegexMatchSetId"]
changetoken = wafclient.get_change_token()["ChangeToken"]
updateregexmatchresponse = wafclient.update_regex_match_set(
                            RegexMatchSetId=regexmatchsetid,
                            Updates=[
                                {
                                    'Action': 'INSERT',
                                    'RegexMatchTuple': {
                                        'FieldToMatch': {
                                            'Type': 'HEADER',
                                            'Data': 'content-type'
                                        },
                                        'TextTransformation': 'NONE',
                                        'RegexPatternSetId': regextpatternsetid
                                    }
                                },
                            ],
                            ChangeToken=changetoken
                        )

print(updateregexmatchresponse)

