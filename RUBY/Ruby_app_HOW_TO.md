
#   Project creation

mkdir PROJECTS/Ruby/test_app
cd PROJECTS/Ruby/test_app

#   Gem manager installation for Ruby

sudo apt update
sudo apt install ruby-full

#   Verify installation

ruby -v

#   Sinatra gem installation

sudo gem install sinatra

#   Other gems installation

sudo gem install rackup puma

#   run the application

ruby app.rb

http://127.0.0.1:4567
