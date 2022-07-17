declare @fator numeric(15,2) = 0.41

if OBJECT_ID('tempdb..##tmp') is not null 
  drop table ##tmp


create table ##tmp
(
	Codigo int,
	GrupoItem varchar(30),
	Tipo		varchar(30)
)

INSERT INTO ##tmp
VALUES 
(1,'_Colhedoras','Tipo_A'),
(2,'_Distribuidor_Ester','Tipo_B'),
(3,'_Feeder_Caminhao','Tipo_C'),
(4,'_Feeder_SC','Tipo_D'),
(5,'_Haybuster','Tipo_E'),
(6,'_Rotormix_Mini','Tipo_F_Mini'),
(7,'_RX 0-11m','Tipo_F_0-11'),
(8,'_RX 0-11m_SC','Tipo_F_0-11_Z'),
(9,'_RX 15-20 m','Tipo_F_15-20'),
(10,'_RX 15-20m_SC','Tipo_F_15-20_Z'),
(11,'_RX 25-27 M','Tipo_F_25-27'),
(12,'_Sega_Pasto','Tipo_G'),
(13,'_TMX 02-5 m','Tipo_H_2-5'),
(14,'_TMX 06-10 m','Tipo_H_6-10'),
(15,'_TMX 12-15 m','Tipo_H_12-15'),
(16,'_Unimix','Tipo_I'),
(17,'_VM 2-8 m','Tipo_J_2-8'),
(18,'_VM 9 m ou >','Tipo_J_9'),
(19,'_Wagon','Tipo_K')


select t1.Codigo as CódigoItem,t1.Tipo Descricao, /*T0.GrupoItem, */CidadeEntrega 'Cidade Entrega',EstadoEntrega 'UF', t0.DataDocumento 'Data Emissão NF',Quantidade,TotalGeral*@fator Valor
from vw_faturamento T0 LEFT JOIN ##tmp T1 ON T0.GrupoItem COLLATE DATABASE_DEFAULT =T1.GrupoItem COLLATE DATABASE_DEFAULT
where TipoItem = 'MÁQUINA' and Quantidade >0 and TotalGeral>0 and NumeroDocumento > 0 and EstadoEntrega not in ('EX', 'EXP') and EstadoEntrega is not null
--collate SQL_Latin1_General_CP850_CI_AS;



--select  DISTINCT GrupoItem
--from vw_faturamento
--where TipoItem = 'MÁQUINA'