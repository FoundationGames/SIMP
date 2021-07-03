# SIMP (for Discord)
### Specialized Image Manipulation Program

SIMP is a very simple and experimental discord bot written in python for some quick image manipulation tasks. <br/>
It should be run privately as it's programmed to only handle one manipulation task at once. <br/> 
Use of async tasks is planned, however to keep the load light while running locally it's configured this way.
<br/>
<br/>
Current commands: <br/>
`s#contentawarescale <amount - between 0.0 and 1.0> <axis - "x" or "y"> <user - optional user mention to use avatar>`
- Either uses your avatar, the specified user's avatar, or an attached file and performs a content-aware scale on the image to the specified amount on the specified axis.
- Aliases: `s#cair`, `s#cas`