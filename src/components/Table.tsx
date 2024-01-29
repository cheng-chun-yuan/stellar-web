import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
  
  export function TransactionsTable({transactions}: {transactions: any[]}) {
    console.log(transactions);
    const transformedData = transactions.map((item) => {
        const keyArray = Object.keys(item)[0].match(/[\w]+/g); // Extracts words from the string
        if (!keyArray) return;
        return {
            name: keyArray[0] ? keyArray[0] : '',
            telecom_pay: keyArray[1]? keyArray[1] : '',
            telecom_receive: keyArray[2]? keyArray[2] : '',
            usage: item[Object.keys(item)[0]]
        };
    });
    return (
      <Table>
        <TableCaption>A list of your recent transaction.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">name</TableHead>
            <TableHead>telecom_pay</TableHead>
            <TableHead>telecom_receive</TableHead>
            <TableHead className="text-right">Amount</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {
    transformedData.map((transaction, index) => (
        transaction ? (
            <TableRow key={index}>
              <TableCell className="font-medium">{transaction.name}</TableCell>
              <TableCell>{transaction.telecom_pay}</TableCell>
              <TableCell>{transaction.telecom_receive}</TableCell>
              <TableCell className="text-right">{transaction.usage}</TableCell>
            </TableRow>
        ) : (
            // Render something else or nothing if transaction is null
            null
        )
    ))
}
        </TableBody>
      </Table>
    )
  }
  