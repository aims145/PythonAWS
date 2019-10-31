import boto3

from ProfileSetup import ProfileSetup

credprofile = ProfileSetup("devl")
assumedRoleObject = credprofile.assumerole()
#print(assumedRoleObject)
wafclient = boto3.client('waf-regional', region_name='us-east-1', aws_access_key_id=assumedRoleObject["Credentials"]["AccessKeyId"], aws_secret_access_key=assumedRoleObject["Credentials"]["SecretAccessKey"], aws_session_token=assumedRoleObject["Credentials"]["SessionToken"]) 
changetoken = wafclient.get_change_token()["ChangeToken"]
print(changetoken)
response = wafclient.create_regex_pattern_set( Name='FileUploadMultiPart', ChangeToken=changetoken )
print(response)
regexpatternct = response["ChangeToken"]
regextpatternsetid = response["RegexPatternSet"]["RegexPatternSetId"]
updateregexresponse = wafclient.update_regex_pattern_set(
                       RegexPatternSetId=regextpatternsetid,
                       Updates=[
                               {
                                   'Action': 'INSERT',
                                   'RegexPatternString': 'multipart/form-data*'
                                },
                           ],
                       ChangeToken=regexpatternct
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
                            RegexMatchSetId='string',
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
