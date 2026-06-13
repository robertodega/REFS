- OS folder creation

        mkdir ~/docker-windows && cd ~/docker-windows

- OS image download

        Windows11
                curl -L -o windows11.iso "https://archive.org/download/win-11-23-h-2-english-x-64/Win11_23H2_English_x64.iso"
        Windows10
                curl -L -o windows10.iso "https://archive.org/download/win-10-22-h-2-italian-x-64/Win10_22H2_Italian_x64.iso"

- KVM virtualization check

        ls -l /dev/kvm && echo "KVM è attivo e pronto!" || echo "KVM NON è attivo"

- QCOW2 format disk generation

        docker run --rm -v "$(pwd)":/data docker.io/tianon/qemu qemu-img create -f qcow2 /data/win11-disk.qcow2 50G

- QEMU Container activation

        - KVM is active
        
                docker run -d \
                  --name windows11-custom \
                  --net host \
                  -v "$(pwd)":/data \
                  docker.io/tianon/qemu \
                  qemu-system-x86_64 \
                    -m 4G \
                    -smp 2 \
                    -drive file=/data/win11-disk.qcow2,if=ide,format=qcow2 \
                    -cdrom /data/windows11.iso \
                    -vnc :0

        - KVM is NOT active

                docker run -d \
                  --name windows11-no-kvm \
                  --net host \
                  -v "$(pwd)":/data \
                  docker.io/tianon/qemu \
                  qemu-system-x86_64 \
                    -m 4G \
                    -smp 2 \
                    -drive file=/data/win-disk.qcow2,if=ide,size=50G,format=qcow2 \
                    -cdrom /data/windows11.iso \
                    -vnc :0

- Client VNC open ( Remmina - Remote Desktop connection)

- Browser access

        http://127.0.0.1:5900

        Windows installation program run ...


- Container Management

    -   Stop

            docker stop <CONTAINER_NAME>
    -   Reboot

            docker start <CONTAINER_NAME>

    -   System Uninstall with virtual disk removal

            docker rm -f <CONTAINER_NAME>
            docker volume rm <CONTAINER_NAME>-disk

