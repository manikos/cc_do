**DO NOT FORGET TO ADD THE vault.yml FILE UNDER THE ./group_vars/all/ directory!!!**

This file is encrypted using [ansible-vault](https://docs.ansible.com/ansible/2.4/vault.html#creating-encrypted-files) command.

It must contain the following keys:

| Keys              | Description |
| ----------------- |-------------|
| `user_group`      | user's group (usually same as `user_name`) |
| `user_name`       | user's username |
| `user_salt`       | a random string of up to 8 characters [a-zA-Z0-9./] |
| `user_pwd`        | user's password (used for `sudo` commands) |
| `user_comment`    | user's full name (optional) |
| `bb_user`         | your bitbucket username |
| `bb_pwd`          | your bitbucket password |
| `db_user`         | production postgres database user (usually the same a `user_name`) |
| `db_pwd`          | production postgres database password |
    
For example, a `vault.yml` file could look like this:
    
---

user_group: mike
user_name: mike
user_salt: aThko86z
user_pwd: mikeSudoPassword
user_comment: Mike Michael
bb_user: mike
bb_pwd: mikeBitBucketPwd
db_user: mike
db_pwd: mikePostgresPwd
            
Usually, you want the same values for every project you deploy, in order not to get lost when you must `ssh` in the server. 
So, create this `vault.yml` file once and then forget about it. 

**Just don't forget the password in case you have to edit/view `vault.yml`**!

