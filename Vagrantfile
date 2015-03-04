# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = 'ejrf'
  config.vm.box_url = "~/vagrantBoxes/ubuntu-14.04.box"

  config.vm.synced_folder ".", "/vagrant", type: "nfs"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.network :public_network, :bridge => 'en0: Wi-Fi (AirPort)'
  config.vm.network "private_network", ip: "192.168.50.4"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box

    config.cache.synced_folder_opts = {
      type: :nfs,
      mount_options: ['rw', 'vers=3', 'tcp', 'nolock']
    }
  end

  config.vm.provision "ansible" do |ansible|
     ansible.playbook = "infrastructure/server.yml"
  end
end
