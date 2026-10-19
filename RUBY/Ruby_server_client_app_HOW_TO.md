
#   Project creation

mkdir PROJECTS/Ruby/server_client_app
cd PROJECTS/Ruby/server_client_app

#   Gem manager installation for Ruby

sudo apt update
sudo apt install ruby-full

#   Verify installation

ruby -v

#   Sinatra gem installation

sudo gem install sinatra

#   Other gems installation

sudo gem install rackup puma

#   Server creation

touch server.rb

#   Client creation

touch client.rb

#   Server execution in a terminal

ruby server.rb

#   Client execution in another terminal

ruby client.rb
