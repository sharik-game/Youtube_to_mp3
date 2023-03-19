class Desc:
    def __init__(self, version: str = "0.0.1"):
        self.version = version
    def desc(self) -> str:
        return  """
# YouTube to mp3  
This online converter can:  
* **Convert youtube video to mp3 file**  
* **Convert mp4 file to mp3 file**    
# For developers
I'm begginer web developer, that's why I will be glad to hear your suggestions  
## P.S
_Website is still under development_  
But you can use converter mp4 to mp3
        """
    def ver(self) -> str:
        return self.version
        
