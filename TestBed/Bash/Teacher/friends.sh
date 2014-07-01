# This is a program that keeps your address book up to date.

friends="Prajwal Sanket Raghu Prakhar Aryaveer"
echo $friends
read name
read gender

if [[ $friends == *"$name"* ]]; then
  echo "You are already there!"
  exit 0
elif [ "$gender" == "m" ]; then
  echo "You are added to Michel's friends list."
  exit 0
else
  echo "You are added to Michel's friends list.  Thank you so much!"
fi
