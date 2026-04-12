create schema if not exists eventos_pro_db;

create table usuario(
idUsuario int primary key auto_increment not null,
nombreUsuario varchar(255) not null unique,
contrasenia varchar(255) not null unique,
rol varchar(10) not null);

create table cliente(
idCliente int primary key auto_increment not null,
nombre varchar(255),
email varchar(255) not null unique,
telefono varchar(15),
nuip varchar(10) not null unique,
idUsuario int,
constraint fkUsuario foreign key cliente(idUsuario) references usuario(idUsuario) on delete cascade on update cascade);

create table coordinador(
idCoordinador int primary key auto_increment not null,
nombre varchar(255),
nuip varchar(10) not null unique,
estado text,
salario double);

create table sede(
idSede int primary key auto_increment not null,
nombre varchar(255),
direccion varchar(255),
capacidad int,
costoAlquiler double);

create table proovedor(
idProovedor int primary key auto_increment not null,
empresa varchar(255),
telefono varchar(15),
email varchar(255) not null unique,
servicioProducto text,
costoServicio double);

create table evento(
idEvento int primary key auto_increment not null,
nombre varchar(255),
fecha date,
estadoEvento text,
estadoPago text,
presupuesto double,
idCliente int,
idCoordinador int,
idSede int,
constraint fkCliente foreign key evento(idCliente) references cliente(idCliente) on delete cascade on update cascade,
constraint fkCoordinador foreign key evento(idCoordinador) references coordinador(idCoordinador) on delete cascade on update cascade,
constraint fkSede foreign key evento(idSede) references sede(idSede) on delete cascade on update cascade);

create table detalles_evento(
idDetalles int primary key auto_increment not null,
costoEvento double,
idEvento int,
idProovedor int,
constraint fkEvento foreign key detallesEvento(idEvento) references evento(idEvento) on delete cascade on update cascade,
constraint fkProovedor foreign key detallesEvento(idProovedor) references proovedor(idProovedor) on delete cascade on update cascade);