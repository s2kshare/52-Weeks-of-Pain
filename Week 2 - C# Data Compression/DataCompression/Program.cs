using System.Text;
using DataCompression;

Console.WriteLine(new string('-', 25));
Console.WriteLine("    DATA COMPRESSION     ");
Console.WriteLine(new string('-', 25));

// Global Vairables
string path = "C:\\Users\\2022000602\\Downloads\\52-header.png";
Logger log = new Logger();

try
{
    byte[] fileBytes = File.ReadAllBytes(path);
    log.Log("FileRead", $"File read successfully! Byte array length: {fileBytes.Length}");

    string output = CompressData(fileBytes);

    string output_file = "./output_c.s2k";
    string original_file = "./output_o.s2k";

    Comparison(output_file, original_file, fileBytes, output);
}
catch (Exception ex)
{
    log.Log("ERROR", ex.Message);
}

void Comparison(string output_file, string original_file, byte[] fileBytes, string compressedstr)
{
    if (!File.Exists(output_file))
    {
        using (FileStream fs = File.Create(output_file))
        {
            using (StreamWriter writer = new StreamWriter(fs))
            {
                writer.Write(compressedstr);
            }
        }
        log.Log("CHECK", "Created Compressed file!");
    }
    if (!File.Exists(original_file))
    {
        using (FileStream fs = File.Create(original_file))
        {
            using (StreamWriter writer = new StreamWriter(fs))
            {
                foreach (byte b in fileBytes)
                {
                    writer.Write(b + " ");
                }
            }
        }
        log.Log("Check", "Created Original file!");
    }

    // Comparison of size
    FileInfo compressedInfo = new FileInfo(output_file);
    FileInfo generalInfo = new FileInfo(original_file);

    if (compressedInfo.Exists && generalInfo.Exists)
    {
        long compressed_size = compressedInfo.Length;
        long original_size = generalInfo.Length;


        log.Log("Size", $"Original   >> {original_size}");
        log.Log("Size", $"Compressed >> {compressed_size}");

        if (compressed_size > original_size)
        {
            log.Log("Output", "Failed Compression");
        }
        else if (compressed_size < original_size)
        {
            log.Log("Output", "Successful Compression");
        }
        else
        {
            log.Log("Output", "No compression applied");
        }
    }
}

static string CompressData(byte[] data)
{
    StringBuilder str = new StringBuilder();
    int count = 1;

    for (int i = 0; i < data.Length; i++)
    {
        if (i == 0)
        {
            if (data[i + 1] == data[i])
            {
                count++;
            }
            else
            {
                str.Append(data[i] + ",");
            }
        }
        else
        {
            if (i != data.Length - 1)
            {
                if (data[i] == data[i + 1])
                {
                    count++;
                }
                else
                {
                    if (count == 1)
                    {
                        str.Append(data[i] + ",");
                    }
                    else
                    {
                        str.Append(count + ":" + data[i] + ",");
                    }
                    count = 1;
                }
            }
            else
            {
                if (count == 1)
                {
                    str.Append(count + ":" + data[i]);
                }
                else
                {
                    str.Append(data[i]);
                }
            }
        }
    }

    return str.ToString();
}
