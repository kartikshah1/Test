# This is a program that keeps your address book up to date.

friends="Prajwal Sanket Raghu Prakhar Aryaveer"
echo $friends
read name
read gender

if [[ $friends == *"$name"* ]]; then
  echo "You are already there!!"
elif [ "$gender" == "m" ]; then
  echo "You are added to Michel's friends list."
else
  echo "You are added to Michel's friends list. Thank you so much!"
fi