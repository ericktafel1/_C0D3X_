> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > MongoDB`

```
mongo "mongodb://localhost:27017"
```
```
> use <DATABASE>;
> show tables;
> show collections;
> db.system.keys.find();
> db.users.find();
> db.getUsers();
> db.getUsers({showCredentials: true});
> db.accounts.find();
> db.accounts.find().pretty();
> use admin;
```
```
> db.getCollection('users').update({username:"admin"}, { $set: {"services" : { "password" : {"bcrypt" : "$2a$10$n9CM8OgInDlwpvjLKLPML.eizXIzLlRtgCh3GRLafOdR9ldAUh/KG" } } } })
```


## Connection

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > MSSQL > Connection`

```
sqlcmd -S <RHOST> -U <USERNAME> -P '<PASSWORD>'
impacket-mssqlclient <USERNAME>:<PASSWORD>@<RHOST> -windows-auth
```
