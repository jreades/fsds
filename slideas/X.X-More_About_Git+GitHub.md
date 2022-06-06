Just to clarify:

- Think of the programming environment (Vagrant+JupyterLab) as being an application (like Word or Excel) that allows you to read/write/edit particular types of files on your home machine.
- Think of GitHub as being like Dropbox (somewhere in the cloud that files on your home machine can be backed up).
- So you should *not* need to do anything in JupyterLab to move files to, or see changes on, GitHub.

So your workflow should be:

1. Save edits to Jupyter notebook.
2. Run `git add <filename.ipynb>` to record changes to the notebook (obviously replace `<filename.ipynb>` completely with the notebook filename.
3. Run `git commit -m "Adding notes based on lecture"` (or whatever `m`essage is appropriate.
4. `git push` to push the changes to GitHub.

If any of those commands indicate that there are no changes being recorded/pushed then it might be that you’re not editing the file that you think you are (this happens to me!).On the GitHub web site you may need to force reload the view of the repository: Shift + Reload button usually does it in most browsers. You may also need to wait 5 to 10 seconds for the changes to become ‘visible’ before reloading. It’s not quite instantaeous.

I don’t know if this will help, but *one* way to think of this is like a kind of Dropbox where *you* control which files get synched (git add+commit) and when (git push/pull), with each repository as a separate Dropbox. So one directory synchs only my teaching in the i2p repository, another synchs only my ML code for my Urban Studies article, etc. Each is a separate repository. Some I haven’t synched in over a year. Some I synched 20 times today.

So, when you cloned the repository from GitHub that I asked you set up, then you basically set up a link between GitHub and your computer. You now do *most* of your work directly on your own computer and *push* it to GitHub. Once in a while, for a very quick edit you might use GitHub’s own web editor instead, but that’s as likely to cause problems as solve them. So you should focus on how you use Git on your *own* machine and then push changes up.

I’ve just realised that what might be confusing you is that when we download the notebook from *my repository* using a web browser you are expecting it to still have some connection to my repository or to develop some connection to your repository. It has neither. When you clicked that download button you were just downloading a file from a web site like any other.

Let’s say that the notebook was called notebook.ipynb; to start tracking it and using it with git you now need to:



- Move it to the folder on *your* computer where *you* have cloned your *own* GitHub repository (let’s say that you called it ‘i2p-student’ and it’s in your Documents directory), so you would do *something* like:
  mv ~/Downloads/notebook.ipynb ~/Documents/i2p-student/
- Now you need to start tracking it:
  git add notebook.ipynb
  git commit -m “Added."
- And now you push it up to GitHub:
  git push
- And if you visit [GitHub.com](GitHub.com) and navigate to your repository under your account you should see the file.


The communication is bi-directional between Git on your computer and GitHub once you have the connection established using git clone https://github.com/<username/whatever your private GitHub repo name is>.git

You get the URL for cloning by clicking on the green button visible in your GitHub repository and selecting ‘https’ as the protocol.

That’s ‘it’.[1]

Jon

[1] I realise that none of this is easy.