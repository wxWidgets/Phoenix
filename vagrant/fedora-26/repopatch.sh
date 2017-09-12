for i in `ls /etc/yum.repos.d/fedora.repo /etc/yum.repos.d/fedora-update*.repo`
do
	sed -i "s/^#metalink=/metalink=/g" $i
	sed -i "s/^baseurl=/#baseurl=/g" $i
done
