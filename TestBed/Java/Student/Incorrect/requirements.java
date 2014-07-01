
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class requirements
{
    private static Map <String, Long> solutions = new HashMap <String, Long> ();

    private static boolean [][] constraints;

    private static long solve (int n, int [] low, int [] high)
    {
        StringBuilder sb = new StringBuilder ();

        for (int i = 0; i < n; i++)
        {
            sb.append (low [i]);
            sb.append (high [i]);
        }

        String signature = sb.toString ();

        Long result = solutions.get (signature);
        if (result == null)
        {
            result = Long.valueOf (doSolve (n, low, high));
            solutions.put (signature, result);
        }

        return result.longValue ();
    }

    private static long doSolve (int n, int [] low, int [] high)
    {
        if (n == 0) return 1;
        else
        {
            long result = 0;

            for (int i = low [n - 1]; i <= high [n - 1]; i++)
            {
                int [] l = new int [n - 1];
                int [] h = new int [n - 1];

                for (int j = 0; j < n - 1; j++)
                {
                    l [j] = constraints [n - 1][j] ? Math.max (low [j], i) : low [j];
                    h [j] = constraints [j][n - 1] ? Math.min (high [j], i) : high [j];
                }

                result += solve (n - 1, l, h)%1007;
            }
            result %= 1000;

            return result;
        }
    }

    public static void main(String[] args) throws Exception
    {
        BufferedReader reader =
            new BufferedReader (
                new InputStreamReader(System.in));

        String nm = reader.readLine ();
        String [] pair = nm.split(" ");
        int n = Integer.parseInt(pair [0]);
        int m = Integer.parseInt(pair [1]);

        constraints = new boolean [n][];
        for (int i = 0; i < n; i++)
            constraints [i] = new boolean [n];

        int [] low = new int [n];
        int [] high = new int [n];
        for (int i = 0; i < n; i++)
            high [i] = 9;

        for (int i = 0; i < m; i++)
        {
            String ab = reader.readLine();
            pair = ab.split (" ");
            int a = Integer.parseInt(pair [0]);
            int b = Integer.parseInt(pair [1]);
            constraints [a][b] = true;
        }

        System.out.println(solve (n, low, high));
    }
}