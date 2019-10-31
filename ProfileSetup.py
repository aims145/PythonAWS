import boto3

class ProfileSetup():
    def __init__(self, env = ""):
        self.env = env
        print("Preparing AWS Profile")
        if self.env == "devl":
            self.rolearn = ""
                                 
        
    def assumerole(self):
        client = boto3.client('sts')
        
        response = client.assume_role(RoleArn = self.rolearn, RoleSessionName = 'AssumeRole')
        
        return response
