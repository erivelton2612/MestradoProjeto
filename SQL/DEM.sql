use SBO_CASALE_PRD

--select t0.itemcode,month(t0.DueDate) , YEAR(t0.DueDate),COUNT(t0.PlannedQty)
--from owor t0
--where OriginNum < 9000000 and YEAR(t0.DueDate)=2021
--group by t0.itemcode,  month(t0.DueDate) , YEAR(t0.DueDate)
--order by 4 desc


--select t0.itemcode,month(t0.DueDate) , YEAR(t0.DueDate),COUNT(t0.PlannedQty)
--from owor t0
--where OriginNum < 9000000 and YEAR(t0.DueDate)=2021

select count(*)
from OWOR t0
where t0.ProdName like '%rx-65%'  
	and YEAR(t0.DueDate)=2021 and  month(t0.DueDate)=6


select --t2.IDItem, 
		'8',
		Qt_Dias_Uteis_Mes,sum(t0.PlannedQty) 'Qtd'
from OWOR t0 left join DataWarehouse.dbo.Dia_Util t1 on t0.DueDate = t1.Dt_Referencia
	left join DataWarehouse.dbo.nroItens t2 on t0.itemcode=t2.codigo
where --ItemCode = '69168'  
	t0.ProdName like '%rx-65%'  
	and YEAR(t0.DueDate)=2021 and  month(t0.DueDate)=6
group by ItemCode, --DueDate,
	Qt_Dias_Uteis_Mes , t2.IDItem


select IDItem, '0','0'
from DataWarehouse.dbo.nroItens

-----descobrir ID item
--select *
--from DataWarehouse.dbo.nroItens
--where codigo = '68726'