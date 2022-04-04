<h1> Honeywords: Making Password Cracking Detectable </h1>

*Interactive demonstration of the honeywords system described in paper.*  
[*Juels and R. Rivest. "Honeywords: Making password-cracking detectable." In ACM SIGSAC conference on Computer & communications security, 2013*](https://people.csail.mit.edu/rivest/pubs/JR13.pdf)

<h2> Summary </h2>
This paper proposed a method for improving the security of passwords by detecting someone attempted to use honeywords (false password) to login.

<h3> Honeywords generation </h3>

> All users have multiple possible passwords for each account, only one of which is genuine, the others are called honeywords.

Several algorithms (methods) for honeywords generation are mentioned in the paper.
1. Tweaking: Tweak the selected character positions in the password to obtain honeywords.
2. Password-model: Generates honeywords using a probabilistic model of real passwords.
3. Tough nuts: Honeywords list contains several tough nuts. (hashed passwords that the adversary is unable to crack)
4. Take-a-tail: Append random digits to the user-proposed password.
5. Hybrid: The combination of password-model and tweaking methods.

<h3> Honeychecker </h3>

> An auxiliary server that can distinguish the user password from honeywords for the login routine, and will set off an alarm if a honeyword is submitted.

It is a separated system where secret information is stored. The secret information is composed of user index and the
corresponding real password index (per user).  
Communicate with the honeychecker by using command `set` and `check`.

<h3> Working mechanism </h3>

* honeychecker set  
![honeychecker set](/images/honeychecker-set.drawio.svg)

* honeychecker check  
![honeychecker check](/images/honeychecker-check.drawio.svg)

<h2> Other terminologies </h2>

* `sugarword` correct user password.
* `honeyword` false password, acting as a honeypot.
* `sweetwords` containing one sugarword + (k-1) honeywords.
* `shadowfile` hashed password file.
* `table_c` table in honeychecker where secret information stored, including user index and corresponding correct password index.
* `flatness` the adversary’s expected probability of guessing the right password.
